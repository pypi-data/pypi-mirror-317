import subprocess
import textwrap
import os

from .keys import SSHKeypair

# Inherit SSHAccount?
class RadicleAccount():
    def __init__(self, member):
        if 'radicle' not in member.apps:
            raise AttributeError('Member has no Radicle Account')

        self.member = member

    def login(self, password):
        hexstring = self.member.login('radicle', password)
        key = bytes.fromhex(hexstring)

        self.secret_key = key

        return 'session_id'


    def save(self, path='~/.radicle/keys', **kwargs):
        overwrite = kwargs.get('overwrite') or False

        try:
            secret_key, public_key = SSHKeypair(self.secret_key, "radicle", export=True)
        except AttributeError:
            print("You're not logged in!")
            return None

        # These two lines are needed to comply to 
        # the silly ssh_rust crate which demands
        # 70 characters per line.
        reformat = secret_key.strip().split('\n')
        secret_key = reformat[0] + '\n' + textwrap.fill(''.join(reformat[1:-1]), 70) + '\n' + reformat[-1] + '\n'

        savepath = os.path.expanduser(path)
        os.makedirs(savepath, exist_ok=True)

        pubkey_path = os.path.join(savepath, 'radicle.pub')
        seckey_path = os.path.join(savepath, 'radicle')

        if overwrite is False and (os.path.isfile(seckey_path) or os.path.isfile(pubkey_path)):
            print('not overwriting existing keys without "overwrite=True"')
        else:
            with open(pubkey_path, 'w') as f:
                f.write(public_key)
            
            with open(seckey_path, 'w') as f:
                f.write(secret_key)

            os.chmod(seckey_path, 0o600)
            os.chmod(pubkey_path, 0o660)
            get_rad = subprocess.run(['which','rad'], capture_output=True)
            radicle_installed = get_rad.returncode == 0
            if radicle_installed:
                subprocess.run(['rad', 'config', 'init', '--alias', self.member.name], capture_output=True)
            else:
                print('Radicle not installed')
                return None
            

        self.member.accounts['radicle'] = { "id": self.getDID() }
        return savepath

    def getDID(self):
        get_rad = subprocess.run(['which','rad'], capture_output=True)
        radicle_installed = get_rad.returncode == 0
        if radicle_installed:
            results = subprocess.run(['rad', 'self', '--did'], capture_output=True)
            if results.returncode == 0:
                return results.stdout.decode().rstrip()
            else:
                print('no Radicle account available')
                return None
        else:
            print('Radicle not installed')
            return None

