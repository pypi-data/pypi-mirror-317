from elements.core import Element, Collection, Timestamp, Config, TagDict, storage, encrypt, decrypt
from elements.core.storage import SolarPath
from pathlib import Path
from elements.core.libs.bip32 import BIP32, HARDENED_INDEX
from elements.accounts.shamir import Mnemonic, Language, get_phrase, create_shares, recover_mnemonic, recover_from_phrase, Share, ThresholdError
from elements.accounts.keys import keymap

from Crypto.Protocol.KDF import scrypt
import os
from .account import Account
from .npc import NPC
from .member import Member

c = Config.load()

'''

Accounts are Collections that represent a person or actor on 
the system. This person can be a Member who logs in with a 
password, or a Guest who logs in from another server within 
the Solar system.

All accounts have an extended public key (xpub) which can be used
to derive other keys for the account.

Members also have an extended private key (xpriv) as part of their
account, which is password-protected.

'''

class Accounts(Collection):
    default_class = NPC
    directory = "accounts"

    # TODO - This needs to cover the entire range
    # of Solar Accounts - NPC, Guest, Member
    class_map = {
        None: default_class,
        "npc": NPC,
        "member": Member
    }

    pointers = {
        'name': lambda e: e.name,
        'pubkey': lambda e: e.pubkey,
        'path': lambda e: e.path
    }

    buckets = {
        'role': lambda e: e.role
    }

    @classmethod
    def sorting_key(cls, element):
        return element.data.content.get('created_at', -1)

    def dict(self):
        self.update()
        data = {}
        for account in self.content:
            name = account.name
            data[name] = self.find(name).profile.flatten()

        return data

    # We need this so that the Accounts object can accurately
    # load subclasses.
    @classmethod
    def load_account(cls, path):
        acc = path.read('account')
        kind = acc.get('kind')
        account_class = cls.class_map.get(kind) or cls.default_class
        return account_class.load(path)

    @classmethod
    def load(cls, path_string, **kwargs):
        path = SolarPath.to(path_string, dir=True)

        accs = []

        for d in path.dirs:
            account = cls.load_account(d)
            accs.append(account)

        accounts = cls(accs)
        accounts.path = path
        return accounts

    def update(self):
        paths_to_update = self.path.dirs
        for path in paths_to_update:
            exists = self.find(path)
            if exists:
                # TODO - Give this the ability to respond to upgraded classes
                exists.update()
            else:
                acct = self.load_account(path)
                self.add(acct)
