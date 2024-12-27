from elements.core import Config
from .base import Integration
from elements.core.encryption import nonce
from elements.core.libs.musig import schnorr_sign, schnorr_verify
from elements.core.libs import bech32
from elements.core.libs.musig.utils import pubkey_gen

config = Config.load()

host = config.HOST or "localhost"

# Developer Note: since the Account exists at a lower level than 
# Member (i.e. it is not attached to the 'main' Account element),
# we have no knowledge of the Member object as a whole.

# Instead, we go through the actions involved in registration
# at a system level and then hand the data back to the caller.

class Nostr(Integration):
    @classmethod
    def from_nsec(cls, nsec):
        label, key = bech32.decode(nsec)
        return cls(key)

    @property
    def private_key(self):
        return self.key

    @property
    def public_key(self):
        return pubkey_gen(self.key)

    @property
    def nsec(self):
        return bech32.encode('nsec', self.private_key)

    @property
    def npub(self):
        return bech32.encode('npub', self.public_key)

    # When a Solar Account is registered, it becomes possible
    # to publish data to the wider network. The account's profile
    # and any shared posts become available to the public.
    def register(self, member):
        public_key = self.public_key.hex()
        address = f'{member.name}@{host}'

        profile_updates = {
            'account': { 'pubkey': public_key },
            'tags': [['i', f'solar:{address}', public_key]],
            'address': address
        }

        return profile_updates

    # Exports the keypair in a designated format
    def keypair(self, fmt="hex"):
        if fmt == "bech32":
            secret_key = bech32.encode('nsec', self.private_key)
            public_key = bech32.encode('npub', self.public_key)
        elif fmt == "bytes":
            secret_key = self.private_key
            public_key = self.public_key
        elif fmt == "hex":
            secret_key = self.private_key.hex()
            public_key = self.public_key.hex()
        else:
            private_key = None
            public_key = None

        return (secret_key, public_key)
        
    def sign(self, data: bytes): 
        # Parse from hex if necessary
        if isinstance(data, str):
            data = bytes.fromhex(data)

        aux_rand = nonce()
        sig = schnorr_sign(data, self.private_key, aux_rand)
        return sig

    def verify(self, msg: bytes, sig: bytes):
        # Parse from hex if necessary
        if isinstance(msg, str):
            msg = bytes.fromhex(msg)

        if isinstance(sig, str):
            sig = bytes.fromhex(sig)

        return schnorr_verify(msg, self.public_key, sig)

    def encrypt(self, data, private_key): pass
    def decrypt(self, data, private_key): pass
