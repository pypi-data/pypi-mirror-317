import unittest

from elements.accounts import Account
from elements.sessions import Sessions
from elements.messages import Conversation, Conversations

from elements.accounts.utilities import lookup
from elements.testing.utilities import enable_test_data, delete_test_data

class TestMessages(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        enable_test_data()
        cls.m1 = Account.register(name="test1")
        cls.m2 = Account.register(name="test2")
        cls.m3 = Account.register(name="test3")
        cls.m1.save()
        cls.m2.save()
        cls.m3.save()

    #def test_new_conversation(self):
    #    convo = Conversation.new('test1', 'test2')
    #    convo.auth('test1', self.s1.content.get('solar'))
    #    convo.message(content="Hi!", author="test1")
    #    self.assertEqual(convo.components[0].message, "Hi!")

    #def test_save_load(self):
    #    convo = Conversation.new('test1', 'test2')
    #    convo.auth('test1', self.s1.content.get('solar'))
    #    convo.message(content="Hi!", author="test1")
    #    convo.message(content="Hello!", author="test2")

    #    # Conversations save automatically, so this isn't
    #    # actually necessary.
    #    path = convo.save()

    #    convo2 = Conversation.load(path)
    #    self.assertEqual(convo2.components[0].message, None)

    #    convo2.auth('test2', self.s2.content.get('solar'))
    #    self.assertEqual(convo2.components[0].message, "Hi!")
    #    self.assertEqual(convo2.components[1].message, "Hello!")
    #    self.assertEqual(len(convo2.messages()), 2)

    #def test_conversations(self):
    #    convo = Conversation.new('test1', 'test2')
    #    convo.message(content="Heyoooo", author="test1")
    #    convo2 = Conversation.new('test1', 'test3')
    #    cl = Conversations.load(self.s1)

    #    same_convo = cl.find(convo.name)
    #    self.assertEqual(convo.id, same_convo.id)
    #    same_convo.message(content='hi', author="test2")

    #    key = cl.lookup_names('test3', size=2)
    #    self.assertEqual(convo2.name, key)
        
    @classmethod
    def tearDownClass(cls):
        delete_test_data()
