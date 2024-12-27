import unittest
from elements.accounts import NPC, Accounts
from elements.places import Place, Places

from elements.testing.utilities import enable_test_data, delete_test_data

class TestPlaces(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        enable_test_data()
        cls.m = NPC.register(name='test')
        m = cls.m.save()

        cls.p1 = Place.new(name="Credenso Café")
        cls.p2 = Place.new(name="The Vineyard")

        cls.p1.save()
        cls.p2.save()

    def test_place_generation(self):
        p = Place.new(name="Tofino", lng=-125.9047080, lat=49.1529643, author=self.m)
        self.assertEqual(p.name, 'tofino')
        self.assertEqual(p.display_name, 'Tofino')
        self.assertEqual(p.pubkey, self.m.pubkey)

    def test_save_load(self):
        p = Place.load(self.p1.path)
        self.assertEqual(self.p1.id, p.id)

    def test_places(self):
        pl = Places.all()
        p = pl.find('credenso-cafe')
        self.assertEqual(p.id, self.p1.id)

    @classmethod
    def tearDownClass(self):
        self.m.unsave()
        self.p1.unsave()
        self.p2.unsave()
        delete_test_data()
