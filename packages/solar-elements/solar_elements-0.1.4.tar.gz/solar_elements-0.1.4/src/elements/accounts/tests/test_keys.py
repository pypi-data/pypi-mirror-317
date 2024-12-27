import unittest
from elements.accounts.integrations.ssh import SSH

seckey1 = '''
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACA7aie8zrakLWKjqNAqbw1zZTIVdx3iQ6Y6wEihi1naKQAAAIgAAAAAAAAA
AAAAAAtzc2gtZWQyNTUxOQAAACA7aie8zrakLWKjqNAqbw1zZTIVdx3iQ6Y6wEihi1naKQ
AAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADtqJ7zOtqQtYqOo0CpvDXNl
MhV3HeJDpjrASKGLWdopAAAAAAECAwQF
-----END OPENSSH PRIVATE KEY-----
'''

seckey2 = '''
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACD8QBQ+h5M/hC8BIdOwG3ad5UzQKWevBfewJj298NNqqgAAAIgAAAAAAAAA
AAAAAAtzc2gtZWQyNTUxOQAAACD8QBQ+h5M/hC8BIdOwG3ad5UzQKWevBfewJj298NNqqg
AAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMfxAFD6Hkz+ELwEh07Abdp3l
TNApZ68F97AmPb3w02qqAAAAAAECAwQF
-----END OPENSSH PRIVATE KEY-----
'''

class TestKeygen(unittest.TestCase):
    def test_ssh(self):
        seckey, pubkey = SSH(bytes(32)).export()
        self.assertEqual(pubkey.rstrip(), 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIDtqJ7zOtqQtYqOo0CpvDXNlMhV3HeJDpjrASKGLWdop')
        self.assertEqual(seckey.strip(), seckey1.strip())
    
        seckey, pubkey = SSH(bytes(31) + b'1').export()
        self.assertEqual(pubkey.rstrip(), 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIPxAFD6Hkz+ELwEh07Abdp3lTNApZ68F97AmPb3w02qq')
        self.assertEqual(seckey.strip(), seckey2.strip())

