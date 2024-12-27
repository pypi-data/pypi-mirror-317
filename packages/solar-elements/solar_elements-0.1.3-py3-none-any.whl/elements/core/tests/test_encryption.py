import unittest

from elements.core.encryption import encrypt, decrypt, decrypt_or, shared_key, nonce
from secp256k1 import PrivateKey

class TestEncryption(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.k1 = nonce()
        cls.k2 = nonce()

        cls.p1 = PrivateKey(cls.k1, raw=True)
        cls.p2 = PrivateKey(cls.k2, raw=True)

    def testSymmetricEncryption(self):
        message = "testing 123"
        enc = encrypt(message, self.p1.private_key)
        dec = decrypt(enc, self.p1.private_key)
        self.assertEqual(dec, message)

        with self.assertRaises(ValueError) as cm:
            decrypt(enc, self.p2.private_key)

        self.assertTrue(str(cm.exception).startswith('MAC'))

    def test_32_byte_aysm(self):
        # Nostr uses 32 byte pubkeys as a standard, which
        # creates some ambiguity about where the key exists
        # on the curve - above or below? We try both options.
        p1_pub = self.p1.pubkey.serialize()[1:].hex()
        p2_pub = self.p2.pubkey.serialize()[1:].hex()

        k1, _ = shared_key(self.p1.private_key.hex(), p2_pub)
        k2, k3 = shared_key(self.p2.private_key.hex(), p1_pub)

        self.assertTrue(k1 == k2 or k1 == k3)

        message = "testing 456"
        enc = encrypt(message, k1)
        dec = decrypt_or(enc, k2, k3)

        self.assertEqual(dec, message)

    def test_33_byte_aysm(self):
        # A 33 byte public key is enough to determine
        # the ecdh with certainty.
        p1_pub = self.p1.pubkey.serialize().hex()
        p2_pub = self.p2.pubkey.serialize().hex()

        k1, _ = shared_key(self.p1.private_key.hex(), p2_pub)
        k2, _  = shared_key(self.p2.private_key.hex(), p1_pub)

        self.assertTrue(k1 == k2)

        message = "testing 789"
        enc = encrypt(message, k1)
        dec = decrypt(enc, k2)

        self.assertEqual(dec, message)
