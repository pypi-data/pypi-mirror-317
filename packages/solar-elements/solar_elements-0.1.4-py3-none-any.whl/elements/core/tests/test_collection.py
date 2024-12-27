import unittest
from elements.core.classes import Element, Collection
from elements.core.storage import identify

class TestCollection(unittest.TestCase):
    def setUp(self):
        first = {'content': 'hello', 'key': 'value', 'd': 'named-element'}
        second = {'content': { 'is_dict': True }, 'key': ['value', 'value2']}
        third = {'content': 'hello', 'key': 'value', 'd': 'other-element'}

        self.el1 = Element(**first)
        self.el2 = Element(**second)
        self.el3 = Element(**third)
        self.c = Collection([first,second])

    def test_get(self):
        el = self.c.find('named-element')
        self.assertEqual(el.content, 'hello')
        el2 = self.c.find('other-element')
        self.assertEqual(el2, None)

    def test_buckets(self):
        c = Collection([self.el1.flatten(),self.el2.flatten(),self.el3.flatten()])
        c.buckets['key'] = lambda e: e.tags.get('key')
        c.remap()
        v = c.find('value', 'key')
        v2 = c.find('value2', 'key')
        self.assertEqual(len(v), 3)
        self.assertEqual(len(v2), 1)

    def test_add(self):
        self.c.add(self.el3)
        self.c.buckets['key'] = lambda e: e.tags.getfirst('key')
        self.c.remap()
        v = self.c.find('value', 'key')
        self.assertEqual(len(v), 3)

if __name__ == "__main__":
    unittest.main()
