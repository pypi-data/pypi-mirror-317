import unittest
from datetime import timedelta
from time import sleep

from elements.accounts import NPC, Accounts
from elements.sessions import Session, Sessions

from elements.testing.utilities import enable_test_data, delete_test_data

class TestSessions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        enable_test_data()

        cls.m = NPC.register("test")
        cls.m.save()
        cls.m2 = NPC.register(name="test2")
        cls.m2.save()

        cls.s = Sessions.all()

        # Here we set the persistence to 1 second so that
        # we don't need to wait 10 hours for the session
        # to expire :)
        Sessions.persistence = timedelta(seconds=1)

    def test_session_creation(self):
        accounts = Accounts.all()
        session = self.s.new(self.m, 'test')

        # key is stored in session.key
        self.assertEqual(session.author.name, 'test')

    def test_session_expiry(self):
        session = self.s.new(self.m, 'test')
        session2 = self.s.new(self.m2, 'test2', persistent=True)
        sleep(1)
        session = self.s.get(session.key)
        session2 = self.s.get(session2.key)
        self.assertEqual(session, None)
        self.assertEqual(session2.author.name, 'test2')

    def test_session_keys(self):
        session = self.s.new(self.m, 'test')
        keyed_session = self.s.get(session.key)
        self.assertEqual(session.id, keyed_session.id)

    @classmethod
    def tearDownClass(cls):
        delete_test_data()
