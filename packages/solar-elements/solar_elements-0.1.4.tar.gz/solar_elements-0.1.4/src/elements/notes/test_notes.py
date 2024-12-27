import unittest

from elements.notes import Note, Notes
from elements.core import Element
from elements.accounts import Member, Accounts
from elements.sessions import Sessions
from elements.testing.utilities import enable_test_data, delete_test_data


class TestNotes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Make the member
        enable_test_data()
        cls.m = Member.register(name="test", master_key=bytes(32))
        path = cls.m.save()
        Accounts.all(reload=True)

        sessions = Sessions.all()

        # Start a session
        session = sessions.new(cls.m, 'test')
        cls.s = session
        
    def test_note_creation(self):
        n = Note(**{ 'content': 'Hello!', 'pubkey': self.s.author.pubkey, 'created_at': "0" })
        n.save()
        self.assertEqual(n.id, '4ee7463bd19cffd2e3ad5d0136542ef80971e4adf5a943d210ceba61d2975c7e')
        n.unsave()

    def test_author_shorthand(self):
        n = Note(**{ 'content': 'Hello!', 'author': self.s.author, 'created_at': "0" })
        self.assertEqual(n.pubkey, self.s.author.pubkey)
        n.unsave()

    def test_note_authorship(self):
        n = Note(**{ 'content': 'Hello!', 'pubkey': self.s.author.pubkey, 'created_at': "0" })
        self.assertEqual(n.author.data.id, self.m.data.id)

    def test_note_publishing(self):
        self.e = Element(**{ 'content': 'Hello!', 'pubkey': self.s.pubkey })
        pub = Note.publish(self.e, self.s)
        path = pub.save()
        new = Note.load(path)
        self.assertTrue(new.verified)
        pub.unsave()

    def test_note_importing(self):
        n = Note(**{ 'content': 'Hello!', 'pubkey': self.s.pubkey })
        with self.assertRaises(AttributeError) as cm:
            event = n.export()

        n.sign(self.s)
        event = n.export()
        imported = Note.import_event(data=event)
        self.assertEqual(n.id, imported.id)
        self.assertTrue(n.verified)
        self.assertTrue(imported.verified)

    # Need to add a test for publishing a note which is replying
    # to another note. Need to add the functionality as well :)
    def test_note_publish_replies(self):
        pass

    @classmethod
    def tearDownClass(cls):
        delete_test_data()
