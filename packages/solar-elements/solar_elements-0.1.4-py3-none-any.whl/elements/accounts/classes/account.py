from elements.core import Element, Collection, Timestamp, Config, TagDict, storage, encrypt, decrypt
from elements.core.storage import SolarPath
from pathlib import Path

from elements.core.libs.bip32 import BIP32, HARDENED_INDEX
from elements.accounts.shamir import Mnemonic, Language, get_phrase, create_shares, recover_mnemonic, recover_from_phrase, Share, ThresholdError
from elements.accounts.keys import keymap

from Crypto.Protocol.KDF import scrypt

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

# AccountData is the structure that holds all of the internal
# data for the account. It looks different depending on the 
# type of account being implemented.
class AccountData(Element):
    kind = "account"

    # Pass a get() to the content body
    def get(self, *args):
        return self.content.get(*args)

# A standard kind 0 metadata element, mostly used for
# social information about the account.
class Profile(Element):
    kind = 0 # NIP-01

    @classmethod
    def new(cls, **data):
        profile = cls.content_dict(**data)
        profile.tags.replace('d', ['profile'])
        return profile

    @property
    def display_name(self):
        return self.content.get('display_name')

    def __getattr__(self, attr):
        return self.content.get(attr)

    def update(self, data):
        return self.content.update(data)

class Account(Collection):
    directory = "accounts"

    class_map = {
        None: AccountData,
        0: Profile
    }

    def __init__(self, *args):
        Collection.__init__(self, *args)
        if len(args) == 0:
            raise IndexError('No data passed to constructor - use .register() to make new accounts')

        xpub_string = self.data.content.get('xpub')
        self.xpub = BIP32.from_xpub(xpub_string)

        self.path = SolarPath.to(self.directory, dir=True) / self.name

    @classmethod
    def sorting_key(cls, *args):
        return True

    @classmethod
    def register(cls, *args, **data):
        raise NotImplementedError("the abstract class 'Account' cannot register new accounts")

    @property
    def data(self):
        for element in self.content:
            if element.name == "account":
                return element

        return None

    @property
    def kind(self):
        # The 'kind' of account ('npc', 'member', 'guest')
        # is represented by the AccountData object
        return self.data.kind

    @property
    def pubkey(self):
        path, _ = keymap['nostr']
        full_key = self.xpub.get_pubkey_from_path(path).hex()

        # Returning 64 bytes (omitting the first one) is the 
        # standard used by nostr and Schnorr-style keys
        return full_key[-64:]

    @property
    def role(self):
        # Returns a list of roles applied to the member.
        return self.data.content.get('role', "").split(':') or ['npc']

    def add_role(self, label):
        roles = self.role
        roles.append(label)
        self.data.content['role'] = ':'.join(roles)
        self.data.save()

    def remove_role(self, label):
        roles = self.role
        try:
            roles.remove(label)

        # remove() will throw an error if the label doesn't
        # exist in the list - which is no problem here
        except ValueError:
            pass

        self.data.content['role'] = ':'.join(roles)
        self.data.save()


    @property
    def profile(self):
        for element in self.content:
            if element.name == 'profile':
                return element

        return None

    def update_profile(self, data):
        self.profile.content.update(data)
        return self.profile

    @property
    def name(self):
        return self.profile.content.get('name')

    @property
    def display_name(self):
        return self.profile.display_name or self.name

    @property
    def is_birthday(self):
        # YYYY-MM-DD or MM-DD
        bday = self.profile.birthday
        if bday is None:
            return None

        today = Timestamp().strftime('%m-%d')

        return bday.endswith(today)

    # Even though it's a collection, there is no need
    # for it to inherit the all() method
    def all():
        pass

    # Returns the account's extended private key. This function
    # will throw an error if the password is incorrect
    def login(self, password) -> BIP32:
        raise NotImplementedError("the abstract class 'Account' cannot login")

    def change_password(self, old_password, new_password):
        raise NotImplementedError("the abstract class 'Account' ")

    def backup(self, recovery_threshold=1, shares=1, language="english"):
        try:
            mnemonic = self.mnemonic
        except AttributeError:
            # backup is only available on a newly created account
            return None

        if recovery_threshold > shares:
            raise ValueError('you need to keep the recovery threshold even with the shares!')

        wordlists = {
            "chinese_simplified": Language.ChineseSimplified,
            "chinese_traditional": Language.ChineseTraditional,
            "czech": Language.Czech,
            "english": Language.English,
            "french": Language.French,
            "italian": Language.Italian,
            "japanese": Language.Japanese,
            "korean": Language.Korean,
            "portuguese": Language.Portuguese,
            "spanish": Language.Spanish
        }

        if shares == 1:
            return get_phrase(mnemonic, wordlists.get(language))
        else:
            backups = []
            shared_phrases = create_shares(recovery_threshold, shares, mnemonic)
            for i in range(shares):
                backups.append(get_phrase(shared_phrases[i], wordlists.get(language)))

            return backups

    @classmethod
    def restore(cls, phrase_array: [[str]],  **kwargs) -> "Account":
        language = kwargs.get('language') or "english"

        wordlists = {
            "chinese_simplified": Language.ChineseSimplified,
            "chinese_traditional": Language.ChineseTraditional,
            "czech": Language.Czech,
            "english": Language.English,
            "french": Language.French,
            "italian": Language.Italian,
            "japanese": Language.Japanese,
            "korean": Language.Korean,
            "portuguese": Language.Portuguese,
            "spanish": Language.Spanish
        }

        # If we are being passed shares, assemble them.
        if len(phrase_array) > 1:
            shares = []
            for phrase in phrase_array:
                shares.append(Share.from_share_phrase(phrase, wordlists[language]))

            mnemonic = recover_mnemonic(shares)
        else:
            mnemonic = recover_from_phrase(phrase_array[0], wordlists[language])

        a = cls.register(master_key=mnemonic.seed, **kwargs)
        return a
    
    def unsave(self):
        if self.path:
            for element in self.content:
                element.unsave()

            storage.delete(self.path)

#class List(Element):
#    kind = 10000
#
#    def __init__(self, data={}):
#        Element.__init__(self, data)
#        self.private = None
#        self.key = None
#
#    def auth(self, key):
#        if not self.content or self.content == "":
#            self.private = TagDict()
#        else:
#            stringy = decrypt(self.content, key)
#            self.private = TagDict(json.loads(stringy))
#
#        self.key = key
#
#    def add(self, entry, private=False):
#        if private:
#            if self.private is None:
#                raise ValueError('need to authenticate first!')
#
#            self.private.add(entry)
#
#        else:
#            self.tags.add(entry)
#
#    def remove(self, key, private=False):
#        if private:
#            if self.private is None:
#                raise ValueError('need to authenticate first!')
#
#            self.private.append(entry)
#
#        else:
#            self.tags.add(entry)
#
#    def save(self, **kwargs):
#        # re-encrypt the private data before saving
#        if self.private:
#            private = json.dumps(self.private.flatten())
#            self.content = encrypt(private, self.key)
#
#        return super().save(**kwargs)
#
#    @property
#    def items(self):
#        # If there are private values, combine them into a 
#        # new TagDict. Otherwise, return the regular one.
#        if self.private:
#            tags = self.tags.flatten()
#            tags.append(*self.private.flatten())
#            return TagDict(tags)
#        else:
#            return self.tags
