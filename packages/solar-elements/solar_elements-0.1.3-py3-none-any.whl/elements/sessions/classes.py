import os
import json
import base64
from datetime import datetime, timedelta

from elements.core import request, Element, Collection
from elements.accounts import Account, keymap
from elements.accounts.integrations import Nostr
from elements.notes import Note

'''

Sessions are an important concept for building interactive
websites with login information. A Session element holds
all of the keys for a particular member, 

This feature of the system allows for maintaining server-side
session data in the form of a dictionary. The sessions dict
stays private, and data is accessed through the methods below.

Sessions can contain private information in the form of
unencrypted keys, and should not be saved to storage.
They will generally also include the Account object for the 
given individual, which is the main way to use these
unencrypted keys.

'''

class Sessions(Collection):
    directory = None
    persistence = timedelta(hours=10)

    pointers = {
        'key': lambda s: s.key
    }

    @classmethod
    def all(cls, *args, **kwargs):
        reload = kwargs.get('reload', False)
        global sessions
        if 'sessions' not in globals() or reload is True:
            sessions = cls()

        return sessions

    # We overwrite the Collection.update() function
    # because Sessions do not have paths.
    def update(self):
        minimum = (datetime.now() - self.persistence).timestamp()

        deleted_keys = []
        
        for session in self.content:
            # When an item in a collection is deleted, the value 
            # is set to "None" to avoid disturbing the list length or
            # index mappings. We skip those values.
            if session is None:
                continue

            expired = session.created_at.timestamp() < minimum and session.persistent == False
            if expired:
                self.delete(session.key, 'key')
                deleted_keys.append(session.key)

        return {'deleted_keys': deleted_keys}

    # We update() before getting an account to make sure that
    # any expired sessions are cleared before the lookup
    def get(self, key, map_name=None):
        self.update()
        index = self.lookup(key, map_name)
        if index is None:
            return None

        return self.content[index]

    def new(self, member, password, **kwargs):
        s = Session(member, password)
        if kwargs.get('persistent') is True:
            s.persistent = True

        self.add(s)
        return s

    def auth(self, member, password):
        # This function pulls the auth key from the member account, 
        # generates an nsec with it and then saves a new session 
        # with the nsec as the session key.
        key = member.data.content.get('auth')
        nsec = Nostr(key).nsec

        s = Session(member, password, key=nsec)
        s.persistent = True
        self.add(s)

        return s

class Session(Element):
    def __init__(self, account : Account, password, key=None):

        bip32 = account.login(password)

        if key is None:
        # Create a random key for session lookup
            self.key = os.urandom(32).hex()
        else:
            self.key = key

        self.notifications = None
        self.conversations = None

        # Delete this session once it expires
        self.persistent = False

        Element.__init__(self, pubkey=account.pubkey, d=account.name)
        self.keychain = bip32
        self.author = account
        self.account = account
        self.profile = account.profile

    @property
    def member(self):
        return self.account

    @property
    def admin(self):
        return "admin" in self.account.role

    # We don't want to persist any session data!
    def save(self, *args, **kwargs): pass

    # Integrations are wrappers around private keys returned
    # from the BIP32 keychain.
    def integration(self, app):
        if self.account.kind is None or self.account.kind == "npc":
            raise AttributeError('Integrations are unavailable for this account type.', self.account.kind)

        path, cls = keymap.get(app)
        if path is None:
            error = f'No integration available for {app}'
            raise ValueError(error)

        key = self.keychain.get_privkey_from_path(path)
        integration = cls(key)
        
        return integration

    # This generic signing function signs a piece of binary data
    # according to the function specified in the integration
    def sign(self, bytestring, app="nostr"):
        integration = self.integration(app)

        return integration.sign(bytestring)

    def authorize(self, url, method="GET"):
        auth = Note({ 'u': url, 'method': method, 'author': self.member.name })
        auth.sign(self)
        assert auth.verified()
        event = auth.export()
        b64 = base64.b64encode(json.dumps(event).encode())
        return b64.decode()
