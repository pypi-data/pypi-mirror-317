from secp256k1 import PrivateKey
from .integrations import Lightning, Nostr, SSH

# This keymap maps the name of an application to an integration object which
# implements key functions such as signing and keypair generation

keymap = {
        'lightning':    ('m/0', Lightning),
        'nostr':        ('m/1', Nostr),
        'ssh':          ('m/2', SSH),
        'solid':          ('m/2', 'ed25519'),
        'radicle':        ('m/3', 'ed25519'),
        'ouroboros':      ('m/4', 'X.509')
}

