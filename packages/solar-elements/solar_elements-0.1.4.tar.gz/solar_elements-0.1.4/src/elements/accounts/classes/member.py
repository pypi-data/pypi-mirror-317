from elements.core import Collection, encrypt, decrypt
from elements.core.libs.bip32 import BIP32, HARDENED_INDEX
from .account import Account, Profile, AccountData

from elements.accounts.shamir import Mnemonic, Language, get_phrase, create_shares, recover_mnemonic, recover_from_phrase, Share, ThresholdError
from elements.accounts.keys import keymap

from Crypto.Protocol.KDF import scrypt

'''
   _____________________________     
  |                             |    
  |  SOLAR Member     \  |  /   |    
  |  06/01/2024     `         ` |
  |                 __  /@\  __ |    
  |  Jenkins,           \@/     |    
  |  Leeroy         .         . |    
  |  npuba1b2c3...    /  |  \   |    
  |_____________________________|    
                                     

A Member is a type of Account which holds the keys
to make use of Solar's integrations.

These keys are unlocked with the login function,
and can be passed to integrations through the use
of an active Session object.

Like other accounts, the member account also holds 
profile data, friend lists, conversations, avatar 
& banner information etc.

'''

class MemberData(AccountData):
    kind = "member"

class Member(Account):
    class_map = {
        None: MemberData,
        0: Profile
    }


    '''
    This function is responsible for the registration of new accounts 
    on the Solar system. It operates with the following parameters:

    name: string ---------- Required for naming the account (arg1 or kwarg)
    password: string ------ Optional (defaults to name)
    salt: string ---------- Optional (defaults to name)
    master_key: bytes(32) - Optional (restores account)
    role: string ---------- Optional (defaults to 'npc')

    '''

    @classmethod
    def register(cls, name_as_arg=None, **data):
        name = name_as_arg or data.get('name')
        if name is None:
            raise ValueError('cannot register an account without a name')

        password = data.get('password') or name
        salt = data.get('salt') or name

        key = data.get('master_key')
        if key is None:
            mnemonic = Mnemonic.generate_random()
            key = mnemonic.seed
        else:
            mnemonic = Mnemonic.from_bytes(key)

        seed = BIP32.from_seed(key)

        # This was going to be used to derive the key from the name as well as
        # the seed phrase, but doesn't really seem helpful at the moment

        account_branch = int.from_bytes(name.encode()) % HARDENED_INDEX
        bip32 = BIP32.from_xpriv(seed.get_xpriv_from_path(f"m/{account_branch}'"))
        xpub = bip32.get_xpub()

        # Before we save the xpriv to the account, we encrypt it with
        # the password. In order to do this effectively, we first derive
        # a password_key using the scrypt Key Derivation Function

        password_key = scrypt(password.encode(), salt, 32, N=2**14, r=8, p=1)
        encrypted_xpriv = encrypt(bip32.get_xpriv(), password_key)

        # We list the account under its main nostr pubkey
        path, _ = keymap['nostr']
        pubkey = bip32.get_pubkey_from_path(path)

        init_data = {
            'content': {
                'name': name,
                'role': data.get('role') or 'account',
                'salt': salt,
                'xpub': xpub,
                'xpriv_enc': encrypted_xpriv.decode()
            },
            'pubkey': pubkey.hex(),
            'tags': [['d', 'account']]
        }

        account_data = MemberData(**init_data)
        profile = Profile.new(name=name, pubkey=pubkey.hex())

        account = cls([account_data, profile]) 
        account.mnemonic = mnemonic

        return account

    # Returns the account's extended private key. This function
    # will throw an error if the password is incorrect
    def login(self, password) -> BIP32:
        password_key = scrypt(password.encode(), self.data.content.get('salt'), 32, N=2**14, r=8, p=1)
        data = self.data.content.get('xpriv_enc')
        xpriv = decrypt(data.encode(), password_key)
        return BIP32.from_xpriv(xpriv)

    def change_password(self, old_password, new_password):
        value = self.login(old_password)
        new_password_key = scrypt(new_password.encode(), self.data.content.get('salt'), 32, N=2**14, r=8, p=1)
        new_data = encrypt(value.get_xpriv(), new_password_key)
        self.data.content['xpriv_enc'] = new_data.decode()

    #def set_avatar(self, file):
    #    avatar = Picture.new(file, { 'author': self.name, 'content': 'account avatar', 'dimensions': (128, 128), 'name': 'avatar' })
    #    avatar.save()
    #    self.components[1] = avatar
    #    self.avatar = avatar
    #    url = self.components[1].tags.get('url')[0]
    #    self.update_profile({ 'avatar': url })
    #    return url

    #def set_banner(self, file):
    #    banner = Picture.new(file, { 'author': self.name, 'content': 'account banner', 'name': 'banner' })
    #    banner.save()
    #    self.components[2] = banner
    #    self.banner = banner
    #    url = self.components[2].tags.get('url')[0]
    #    self.update_profile({ 'banner': url })
    #    return url

    # Save a piece of data to the Member's account tags, password encrypted
    #def store_data(self, data, tag_name, password, overwrite=False):
    #    if overwrite is False and self.secret_keys.get(app_name) is not None:
    #        raise ValueError('not overwriting stored key without overwrite=True')

    #    password_key = scrypt(password.encode(), self.salt, 32, N=2**14, r=8, p=1)

    #    data = encrypt(data, password_key)
    #    self.tags.replace(tag_name, [data.decode()])


    #def update_profile(self, data):
    #    if self.profile is None:
    #        # If there is no profile, instantiate it under this member with the passed data
    #        self.components[0] = Profile({ 'author': self.name, 'content': data })
    #        self.profile = self.components[0]
    #    else:
    #        # Otherwise, update the existing data with what was passed.
    #        self.profile.update(data)

    #    return self.profile
