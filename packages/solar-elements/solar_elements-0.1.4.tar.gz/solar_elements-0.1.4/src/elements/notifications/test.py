import unittest
import shutil
from elements.accounts import NPC
from elements.notifications import Notification, Notifications, notify, announce

from elements.testing.utilities import enable_test_data, delete_test_data


class TestNotifications(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        enable_test_data()
        cls.n = Notification.new(content="Check this out!", link='/test/url/')
        cls.n2 = Notification.new(content="Check this out!", link='/test/url2/')
        cls.m = NPC.register(name="test", role="member")
        cls.m.save()
        cls.m2 = NPC.register(name="test2", role="nonmember")
        cls.m2.save()

    def test_generation(self):
        self.assertTrue(self.n.author.name == 'npc')
        self.assertTrue(self.n.tags.get('link')[0].endswith('/test/url/'))

    def test_save_load(self):
        self.n.save()
        path = self.n.path
        n = Notification.load(path)
        self.assertEqual(self.n.id, n.id)
        self.n.unsave()

    def test_marking_as_read(self):
        path = self.n.save()
        new_path = self.n.mark_as_read()
        self.assertNotEqual(path, new_path)

        old = Notification.load(path)
        self.assertEqual(old, None)

        new = Notification.load(new_path)

        # Same id, path updated
        self.assertEqual(new.id, self.n.id)
        self.assertEqual(new.path, self.n.path)
        self.n.unsave()

    def test_collection(self):
        self.assertEqual(Notifications.all(), None)
        nl = Notifications.load('npc')
        self.n.save()
        self.n2.save()
        nl.update()
        self.assertEqual(len(nl.unread), 2)
        self.assertEqual(len(nl.read), 0)

        name = nl.unread[0].name
        n = nl.find(name)
        path = n.mark_as_read()
        self.assertEqual(len(nl.unread), 1)
        self.assertEqual(len(nl.read), 1)
        self.assertEqual(nl.read[0].name, name)

        nl.clear()
        self.assertEqual(len(nl.unread), 0)
        self.assertEqual(len(nl.read), 2)

    def test_notify(self):
        path = notify(self.m, content="Hey!", link="/link/url/")
        n = Notification.load(path)
        self.assertEqual(n.content, "Hey!")
        self.assertEqual(n.author.name, 'test')
        self.assertTrue(n.tags.get('link')[0].endswith('/link/url/'))

    def test_announce(self):
        paths = announce(content="Hey!", link="/link/url/")
        self.assertEqual(len(paths), 1)
        paths = announce(content="Hey!", role="nonmember", link="/link/url/")
        self.assertEqual(len(paths), 1)
        paths = announce(content="Hey!", role="admin", link="/link/url/")
        self.assertEqual(len(paths), 0)
    
    @classmethod
    def tearDownClass(cls):
        delete_test_data()
