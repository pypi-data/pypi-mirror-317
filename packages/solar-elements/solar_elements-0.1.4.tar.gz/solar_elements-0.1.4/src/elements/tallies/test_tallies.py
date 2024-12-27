import unittest
from elements.accounts import NPC, Accounts
from elements.posts import Post
from elements.tallies import Tally, Tallies

from elements.testing.utilities import enable_test_data, delete_test_data

class TestTallies(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        enable_test_data()
        cls.m = NPC.register('test')
        m = cls.m.save()

        cls.p1 = Post(title="Post 1", author=cls.m)
        cls.p2 = Post(title="Post 2", author=cls.m)
        cls.p3 = Post(title="Post 3", author=cls.m)
        cls.p4 = Post(title="Post 4", author=cls.m)

        cls.p1.save()
        cls.p2.save()
        cls.p3.save()
        cls.p4.save()

    def test_tally(self):
        t = Tally.on(self.p1)
        self.assertEqual(t.count, 0)
        t.change(5, self.m)
        self.assertEqual(t.count, 5)
        t.change(-2, self.m)
        self.assertEqual(t.count, 3)
        t.set(11)
        self.assertEqual(t.count, 11)
        from_m = t.from_pubkey(self.m.pubkey)
        self.assertEqual(from_m['count'], 3)
        t.unsave()

    def test_save_load(self):
        t = Tally.on(self.p2)
        t.set(13)
        path = t.save()
        t2 = Tally.load(path)
        self.assertEqual(t.id, t2.id)
        self.assertEqual(t2.count, 13)
        t.unsave()

    def test_tallies(self):
        t = Tally.on(self.p1)
        t.save()
        tl = Tallies.all()
        t2 = tl.find(self.p1.address)
        self.assertEqual(t.id, t2.id)
        t.unsave()

    def test_reload(self):
        t = Tally.on(self.p4)
        t.set(30) 
        t.save()
        t2 = Tally.on(self.p4)
        self.assertEqual(t2.count, 30)
        self.assertEqual(t.id, t2.id)
        t.unsave()

    def test_sums(self):
        t = Tally.on(self.p3)
        t.set(10)
        t.save()
        t2 = Tally.on(self.p2)
        t2.set(15)
        t2.save()
        t3 = Tally.on(self.p2, subject="sats")
        t3.set(1500)
        t3.save()
        tl = Tallies.all()
        self.assertEqual(tl.sum(), 25)
        self.assertEqual(tl.sum('sats'), 1500)
        t.unsave()
        t2.unsave()
        t3.unsave()


    @classmethod
    def tearDownClass(self):
        self.m.unsave()
        self.p1.unsave()
        self.p2.unsave()
        delete_test_data()
