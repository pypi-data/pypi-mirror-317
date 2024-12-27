from elements.core import Collection
from elements.core.libs.bip32 import BIP32
from .account import Account, Profile, AccountData

'''

Not a real account, just here to keep things from breaking

'''

class Placeholder(Account):
    def __init__(self):
        Collection.__init__(self)

    @property
    def data(self):
        return AccountData()

    @property
    def profile(self):
        return Profile()

    @property
    def xpub(self):
        return BIP32.from_seed(bytes(32))

    @property
    def role(self):
        return ['npc']

    @property
    def name(self):
        return 'npc'

    @property
    def display_name(self):
        return 'NPC'

    def add_role(self, label): pass
    def remove_role(self, label): pass

