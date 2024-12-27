import unittest
from elements.core.classes import Element, Collection
from elements.core.storage import identify

class TestElement(unittest.TestCase):
    def setUp(self):
        self.e = Element(**{'content': 'hello', 'key': 'value'})
        self.e2 = Element(**{'content': { 'is_dict': True }, 'key': 'value'})

    def test_attributes(self):
        self.assertEqual(self.e.content, 'hello')
        self.assertEqual(self.e.pubkey, bytes(32).hex())
        self.assertEqual(self.e.kind, None)
        self.assertEqual(self.e.tags['key'], ['value'])

    def test_save_load(self):
        self.assertTrue(self.e.path == None)
        path = self.e.save()
        self.assertFalse(self.e.path == None)
        e_loaded = Element.load(path)
        self.assertEqual(self.e.id, e_loaded.id)

    def test_rehydrate_dict(self):
        self.assertEqual(self.e2.path, None)
        path = self.e2.save()
        self.assertNotEqual(self.e2.path, None)
        e2_loaded = Element.load(path)
        self.assertTrue(e2_loaded.content.get('is_dict'))
        
    def tearDown(self):
        self.e.unsave()
        self.e2.unsave()

if __name__ == "__main__":
    unittest.main()
