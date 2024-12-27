from elements.core import Collection
from elements.core.libs.bip32 import BIP32, HARDENED_INDEX

from elements.accounts.shamir import Mnemonic 
from elements.accounts.keys import keymap

from .account import Account, Profile, AccountData
from .member import Member

from Crypto.Protocol.KDF import scrypt

'''

beep, boop.

An NPC account's data is not password-encrypted, making it unsuitable
for most Solar functionality. These are entry-level accounts which 
can be upgraded by backing up the seed phrase.

'''

class NPCData(AccountData):
    kind = "npc"

class NPC(Account):
    class_map = {
        None: NPCData,
        0: Profile
    }

    @classmethod
    def register(cls, name_as_arg=None, **data):
        name = name_as_arg or data.get('name')
        if name is None:
            raise ValueError('cannot register without a name')

        password = data.get('password') or name
        salt = data.get('salt') or name

        key = data.get('master_key')
        if key is None:
            mnemonic = Mnemonic.generate_random()
            key = mnemonic.seed
        else:
            mnemonic = Mnemonic.from_bytes(key)

        seed = BIP32.from_seed(key)

        # This provides an extra layer of security by deriving the main account key
        # using a hash of the account name. The account can only be properly
        # recovered with the recovery phrase and the name.

        account_branch = int.from_bytes(name.encode()) % HARDENED_INDEX
        bip32 = BIP32.from_xpriv(seed.get_xpriv_from_path(f"m/{account_branch}'"))
        xpub = bip32.get_xpub()

        # Before we save the xpriv to the account, we encrypt it with
        # the password. In order to do this effectively, we first derive
        # a password_key using the scrypt Key Derivation Function

        password_key = scrypt(password.encode(), salt, 32, N=2**14, r=8, p=1)
        #encrypted_xpriv = encrypt(bip32.get_xpriv(), password_key)

        # We list the account under its main nostr pubkey
        path, _ = keymap['nostr']
        pubkey  = bip32.get_pubkey_from_path(path)
        auth    = bip32.get_privkey_from_path(path)

        init_data = {
            'content': {
                'name': name,
                'role': data.get('role') or 'account',
                'salt': salt,
                'xpub': xpub,
                'auth': auth.hex(),
                'hashword': password_key.hex(),
                'seed': key.hex()
            },
            'pubkey': pubkey.hex(),
            'tags': [['d', 'account']]
        }

        account_data = NPCData(**init_data)
        profile = Profile.new(name=name, pubkey=pubkey.hex())

        account = cls([account_data, profile]) 

        return account

    def login(self, password) -> BIP32:
        if password == self.data.content.get('auth'):
            return BIP32.from_xpub(self.data.content.get('xpub'))

        salt = self.data.content.get('salt')
        password_key = scrypt(password.encode(), salt, 32, N=2**14, r=8, p=1)

        # In the case of a None-type login, it means we need to
        # convert the account into an up-to-date format. This 
        # should be deprecated when no longer necessary
        if self.kind is None:
            print('converting account to NPC (elements/accounts/classes/npc.py-login())')
            from elements.core import decrypt
            from elements.accounts.keys import keymap
            path, _ = keymap['nostr']
            new_data = NPCData(**self.data.flatten())
            new_data.kind = "npc"
            xpriv_enc = self.data.tags.getfirst('xpriv')
            del new_data.tags['xpriv']
            xpriv = decrypt(xpriv_enc.encode(), password_key)
            bip32 = BIP32.from_xpriv(xpriv)
            new_data.content['auth'] = bip32.get_privkey_from_path(path).hex()
            new_data.content['hashword'] = password_key.hex()

            for i in range(len(self.content)):
                if self.content[i].name == "account":
                    self.content[i] = new_data

            self.save()
        
        assert password_key.hex() == self.data.content.get('hashword')
        return BIP32.from_xpub(self.data.content.get('xpub'))

    def change_password(self, old_password=None, new_password=None):
        password = new_password or self.name
        password_key = scrypt(password.encode(), self.data.content.get('salt'), 32, N=2**14, r=8, p=1)
        self.data.content['hashword'] = password_key.hex()
        self.save()

    # This operation makes backing up the seed phrase impossible,
    # so proceed with caution. Suggested to make sure that the
    # account owner has proven they hold the seed phrase first

    def upgrade_to_member(self, password=None):
        if password is None:
            password = self.name

        salt = self.data.content.get('salt')
        password_key = scrypt(password.encode(), salt, 32, N=2**14, r=8, p=1)
        assert password_key.hex() == self.data.content.get('hashword')

        seed = self.data.content.get('seed')

        # This only happens with old accounts which were demoted to NPC status
        if seed is None:
            raise AttributeError('cannot upgrade a seedless NPC')

        m = Member.register(
            name       = self.name, 
            password   = password or self.name,
            salt       = salt,
            role       = self.data.content.get('role'),
            master_key = bytes.fromhex(seed)
        )

        # Change the AccountData
        for i in range(len(self.content)):
            if self.content[i].name == "account":
                self.content[i] = m.data

        return self.data
