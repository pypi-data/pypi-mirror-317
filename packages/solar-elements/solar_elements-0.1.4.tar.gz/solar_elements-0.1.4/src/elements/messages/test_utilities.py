import unittest
import subprocess
from time import sleep
import os

from elements.accounts import Account
from elements.messages import Conversation, Conversations
from elements.sessions.utilities import start_session, load_session
from elements.messages.utilities import send_direct_message

from elements.testing.utilities import enable_test_data, delete_test_data

class TestAPIMessaging(unittest.TestCase):
    pass
    #@classmethod
    #def setUpClass(cls):
    #    enable_test_data()

    #    # Create the members
    #    cls.m1 = Account.register(name="test1")
    #    cls.m1.save()
    #    cls.m2 = Account.register(name="test2")
    #    cls.m2.save()

    #    # Start the test server
    #    cls.server = subprocess.Popen(['python', os.path.join('elements','testing','app.py')])

    #    # Open the sessions, register accounts
    #    k1 = start_session('test1', "test1")
    #    k2 = start_session('test2', "test2")
    #    cls.s1 = load_session(k1)
    #    cls.s2 = load_session(k2)

    #    sleep(0.5)

    #def test_start_conversation(self):
    #    send_direct_message(self.s1, "test2@localhost:1618", "Hi!")
    #    cl = Conversations.load(self.s1)
    #    key = cl.lookup_names('test2@localhost:1618')
    #    c = cl.find(key)
    #    self.assertEqual(len(c.messages()), 1)

    #def test_conversation_message(self):
    #    convo = Conversation.new('test1', 'test2')
    #    convo.auth('test1', self.s1.content.get('solar'))
    #    convo.message(content="Hi!", author="test1")
    #    chat = send_direct_message(self.s2, "test1", "Hello!", force_remote="localhost:1618")
    #    chat.auth('test2', self.s2.content.get('solar'))
    #    self.assertEqual(len(chat.messages()), 2)

    #@classmethod
    #def tearDownClass(cls):
    #    cls.server.kill()
    #    delete_test_data()
        
        

