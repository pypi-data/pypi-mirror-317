import unittest
from elements.notes import Note
from elements.accounts import NPC, Accounts
from elements.responses import Response, Responses

from elements.testing.utilities import enable_test_data, delete_test_data

class TestResponses(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        enable_test_data()
        cls.m = NPC.register(name='test')
        m = cls.m.save()
        a = Accounts.all()

        cls.e1 = Note(**{ 'content': 'Hi!', 'pubkey': cls.m.pubkey })
        cls.e2 = Note(**{ 'content': 'Hello!', 'pubkey': cls.m.pubkey })

        cls.e1.save()
        cls.e2.save()

    def test_response_generation(self):
        r = Response.new(target=self.e1, pubkey=self.m.pubkey)
        self.assertEqual(r.author.name, 'test')
        self.assertEqual(r.target.id, self.e1.id)

    def test_save_load(self):
        r = Response.new(target=self.e1)
        path = r.save()
        r2 = Response.load(path)
        self.assertEqual(r.id, r2.id)
        r.unsave()

    def test_response_lookup(self):
        rl = Responses.all()

        r1 = Response.new('+', pubkey=self.m.pubkey, target=self.e1)
        r1.save()

        r2 = Response.new(pubkey=self.m.pubkey, target=self.e2)
        p = r2.save()
        rl.update()

        refs = rl.find(str(self.e1.path.url), "target")
        self.assertEqual(len(refs), 1)
        refs = rl.find(self.m.name, "author")
        self.assertEqual(len(refs), 2)

        r1.unsave()
        r2.unsave()

    @classmethod
    def tearDownClass(self):
        self.m.unsave()
        self.e1.unsave()
        self.e2.unsave()
        delete_test_data()
