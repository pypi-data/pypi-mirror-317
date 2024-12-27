import unittest
from elements.sessions import Sessions
from elements.sessions.utilities import load_session, start_session, auth_session
from elements.accounts import Member
from elements.accounts.integrations import Nostr

from elements.testing.utilities import enable_test_data, delete_test_data

class TestIntegrations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        enable_test_data()
        cls.m = Member.register("test", master_key=bytes(32))
        cls.m.save()

    def setUp(self):
        self.s = Sessions.all()

    def testNostr(self):
        k = start_session('test', 'test')
        s = load_session(k)
        nostr = s.integration('nostr')
        from_nsec = Nostr.from_nsec(nostr.nsec)

        self.assertEqual(nostr.private_key, from_nsec.private_key)
        self.assertEqual(nostr.private_key.hex(), 'cf365342993deeae86c6ff12229a6e7f370759859033a2b8738dfa3bc4d8f813')
        self.assertEqual(nostr.public_key.hex(), 'ac09b06e6eb5e9c253d936624c3c7c9ece14926393dc1773a7842d25978fe5d6')
        self.assertEqual(nostr.nsec, 'nsec1eum9xs5e8hh2apkxlufz9xnw0umswkv9jqe69wrn3harh3xclqfsmq67vg')
        self.assertEqual(nostr.npub, 'npub14symqmnwkh5uy57exe3yc0runm8pfynrj0wpwua8sskjt9u0uhtqff79se')

    #def test_solar_registration(self):
    #    session = self.s.new(self.m,'test')
    #    updates = session.register('solar')
    #    m = session.member
    #    self.assertTrue(m.profile.address != None)

    # I need to make more tests here, but integrations
    # aren't a priority for the upcoming launch

    def tearDown(self):
        self.m.unsave()
        
