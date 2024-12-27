from secp256k1 import PrivateKey

# An Integration is a base class for using a specific private
# key to integrate with other platforms, generating account
# data and allowing for key-specific actions.

class Integration:
    def __init__(self, key):
        if not isinstance(key, bytes):
            key = bytes.fromhex(key)

        self.key = key

    # This function will save a file 
    # to the member's directory
    def register(self, member): pass
    
    def sign(self, bytestring): pass
    def verify(self, bytestring): pass

    def encrypt(self, bytestring): pass
    def decrypt(self, bytestring): pass
