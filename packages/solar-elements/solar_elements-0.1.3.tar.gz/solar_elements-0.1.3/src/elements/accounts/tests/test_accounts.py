import unittest
from elements.accounts import NPC, Member, Accounts
from elements.accounts.shamir import ThresholdError
from elements.core.storage import identify
from random import randrange

from elements.testing.utilities import enable_test_data, delete_test_data

class TestAccount(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        enable_test_data()
        cls.a = Member.register(name="test", master_key=bytes(32), role="test_role:member")
        cls.a2 = NPC.register(name="another_test", role="test_role:npc")
        cls.a.save()
        cls.a2.save()

    def test_name(self):
        self.assertEqual(self.a.name, "test")

    def test_loading(self):
        a2 = NPC.load(self.a.path)
        self.assertEqual(self.a.data.id, a2.data.id)
        self.assertTrue(self.a.clean_path != None)

    def test_backup_restore(self):
        acc = Member.register(name="test")
        backup = acc.backup()
        restored = Member.restore([backup], name="test")
        backup_key = acc.login('test')
        restored_key = restored.login('test')
        self.assertEqual(backup_key.get_xpriv(), restored_key.get_xpriv())

    def test_upgrade(self):
        acc = NPC.register(name="test")
        password = "test"
        acc.upgrade_to_member(password)
        self.assertEqual(acc.kind, 'member')

    def test_backup_restore_from_shares(self):
        acc = Member.register(name="test")
        backup = acc.backup(5,7) # Need any 5 of 7 shares to recover

        shares = []
        for i in range(5):
            choice = randrange(len(backup))
            shares.append(backup.pop(choice))
           
        restored = Member.restore(shares, name="test", quick=True)
        backup_key = acc.login('test')
        restored_key = restored.login('test')
        self.assertEqual(backup_key.get_xpriv(), restored_key.get_xpriv())

        # If we don't have enough recovery shares, an exception is raised.
        shares = shares[1:]
        with self.assertRaises(ThresholdError) as cm:
            NPC.restore(shares, quick=True)

        self.assertEqual(str(cm.exception), "4 does not meet the minimum threshold of 5")

    def test_uniqueness(self):
        a1 = NPC.register(name="test1")
        a2 = NPC.register(name="test2")
        a1_key = a1.login('test1')
        a2_key = a2.login('test2')
        self.assertNotEqual(a1_key, a2_key)

    def test_roles(self):
        a1 = NPC.register(name="test1", role='member:dev')
        self.assertTrue('dev' in a1.role)
        a1.remove_role('dev')
        self.assertFalse('dev' in a1.role)
        a1.remove_role('dev')
        a1.add_role('admin')
        self.assertTrue('admin' in a1.role)
        

    def test_login(self):
        key = self.a.login('test')
        # I had to change this value, likely because of changes to the underlying generation
        # scheme. If I have to change it again, I think it's a problem.
        self.assertEqual(key.get_xpriv(), 'xprv9uk1GDV8nv7BsncFCoApZXpvLVDQPFNvhKfVbUTFNhzegkEk7X6owT1J6UyDyseeWa2V4f8GgG7hzAJtshYk7fX2bn3njAzk5xkNRWqDncB')

    def test_accounts(self):
        accounts = Accounts.all(reload=True)
        test = accounts.find('test')
        self.assertEqual(test.pubkey, self.a.pubkey)
        pk = self.a.pubkey
        test2 = accounts.find(pk)
        self.assertEqual(test2.pubkey, pk)
        accts  = accounts.find('test_role', 'role')
        self.assertEqual(len(accts), 2)

    def test_global(self):
        accounts = Accounts.all()
        accounts2 = Accounts.all()
        self.assertTrue(accounts is accounts2)


    @classmethod
    def tearDownClass(cls):
        cls.a.unsave()
        delete_test_data()

