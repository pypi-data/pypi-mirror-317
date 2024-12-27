from collections import defaultdict

from elements.core import Element, Collection, Config
from elements.core.storage import identify, load_file
from elements.core.libs.musig import schnorr_verify
from elements.accounts.utilities import lookup

from secp256k1 import PublicKey

c = Config.load()

'''

> Notes

Notes are the simplest form of social data that is 
regularly used in the Solar system.

A Note is a non-editable piece of text with an author
associated by their public key. Notes can be posted
to any page on the system, though whether or not
they will be displayed depends on how the page is
constructed.

Notes expand the base structure of Element to
include signatures - allowing for full
integration with the nostr ecosystem through
the export function.

For simplicity, serialized notes will drop any
replies that cannot be resolved to an ID and any
mentions that cannot be mapped to a public key.

'''

class Note(Element):
    kind = 1
    directory = 'notes'
    key_data = ['content', 'author', 'created_at', 'kind', 'tags', 'pubkey', 'id', 'sig', 'filepath']

    # When we initialize a Note, we are assuming that it
    # has been saved in a Solar compliant format by a member
    # with a registered account - meaning they have an
    # available pubkey. 
    def __init__(self, **data):
        # This value is looked up when .author is accessed
        self._author = data.pop('author', None)

        Element.__init__(self, **data)
        s = self.tags.getfirst('s')
        if s is None:
            self.tags.add(['s', c.host])

        if self._author:
            self.pubkey = self._author.pubkey
        else:
            self.pubkey = data.get('pubkey')

        sig = data.get('sig')
        if sig:
            self.sig = bytes.fromhex(sig)
        else:
            self.sig = None

    # Construct a note from standard nostr data.
    # Accepts either 'data={}' or 'path=local/path'
    @classmethod
    def import_event(cls, **kwargs):
        path = kwargs.get('path')
        data = kwargs.get('data')

        if data is None and path is None:
            return None
        elif data is None: 
            data = load_file(path)

        pubkey = data.get('pubkey')
    
        return cls(**data)
        

    # Create a signed note from an existing element and
    # an active session for signing it.
    @classmethod
    def publish(cls, element, session):
        data = element.flatten()
        
        # If the data has a kind of -1, replace it with
        # an appropriate value for publishing
        if data.get('kind') == -1:
            data['kind'] = cls.kind

        note = cls(**data)
        sig = session.sign(note.id)
        note.sig = sig
        return note

    # Sign a newly created note using an active session.
    def sign(self, session):
        sig = session.sign(self.id)
        self.sig = sig
        return sig
        

    # Add the signature to the flattened object.
    def flatten(self):
        el = Element.flatten(self)
        if self.sig:
            el['sig'] = self.sig.hex()
        return el

    # Returns a nostr-compliant form of the flattened
    # value, able to be shared over the network.
    def export(self):
        if self.verified is False:
            raise AttributeError("cannot export an unsigned note")

        el = self.flatten()
        el['pubkey'] = self.pubkey
        el['id'] = self.id

        return el

    # Verifies that the signature from the pubkey is valid for
    # This note's computed id value
    @property
    def verified(self):
        if self.sig is None:
            return False

        pubkey = bytes.fromhex(self.pubkey)
        id_hash = bytes.fromhex(self.id)
        return schnorr_verify(id_hash, pubkey, self.sig)

    @property
    def author(self):
        # Look up the author. If they've been looked up already,
        # return that value.
        if self._author is None:
            self._author = lookup(self.pubkey)
        
        return self._author 

class Notes(Collection):
    directory = "notes"
    default_class = Note

    @classmethod
    def on(cls, element, **data):
        if element.name is None:
            raise ValueError('element has no name')

        if element.path is None:
            raise ValueError('element has no url')

        path = SolarPath.to(cls.directory, dir=True) / element.url
        return cls.load(path)

    # This function organizes a collection of notes
    # into top-level comments and their replies.
    def organize(self, **options):
        session = options.get('session')
        if session:
            op = session.member
        else:
            op = None

        replies = defaultdict(list)
        top_level = []

        last = int(options.get('last') or 0)

        for comment in self:
            if op and (comment.author.name == op.name or "admin" in op.role):
                comment.delete = True
            replying_to = comment.tags.getfirst('e')
            if replying_to is not None:
                replies[replying_to].append(comment)
            else:
                top_level.append(comment)

        for comment in top_level:
            comment.replies = replies[comment.clean_path]

            # We need this so we can refer to it in the template
            comment.reply_target = comment.url

        if last:
            top_level = top_level[:-last]

        return top_level
