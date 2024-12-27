import unittest
import subprocess
from datetime import timedelta
from time import sleep

from elements.accounts import NPC, Accounts#, Guest, Guests
from elements.accounts.utilities import lookup
from elements.accounts.integrations import Nostr
from elements.sessions.utilities import start_session, load_session, auth_session, end_session

from elements.testing.utilities import enable_test_data, delete_test_data

class TestSessions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        enable_test_data()

        cls.m = NPC.register("test")
        pa = cls.m.save()
        cls.m2 = NPC.register("test2")
        cls.m2.save()
        Accounts.all(reload=True)
        #cls.server = subprocess.Popen(["python", "elements/testing/app.py"])
        #sleep(0.5)

    def test_session_creation(self):
        key = start_session('test', 'test')
        session = load_session(key)
        self.assertEqual(session.account.name, "test")

    def test_auth_session(self):
        nostr = Nostr(self.m.data.get('auth'))
        session = auth_session(nostr.nsec)
        self.assertEqual(session.account.name, "test")
        

    #def test_remote_lookup(self):
    #    key = start_session('test', 'test')
    #    session = load_session(key)
    #    session.register('solar')
    #    self.assertTrue(session.member.pubkey != None)

    #    # If we were not setting host to localhost:0 with
    #    # enable_test_data(), this name would be resolved
    #    # locally.
    #    name = 'test@localhost:1618'

    #    # We should not have this user locally
    #    local = lookup(name, request=False)
    #    self.assertEqual(local, None) 

    #    # We should be able to find them by request
    #    acc = lookup(name, request=True, member="test2")

    #    self.assertTrue(isinstance(acc, Guest))
    #    self.assertEqual(acc.author, "test2")

    #    # Once we've looked them up, they're saved
    #    # in the guests directory
    #    local = Guests.all().find(name)
    #    self.assertEqual(acc.id, local.id)

    @classmethod
    def tearDownClass(cls):
        #cls.server.kill()
        delete_test_data()
