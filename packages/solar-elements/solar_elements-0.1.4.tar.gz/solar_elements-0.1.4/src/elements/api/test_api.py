import unittest
import subprocess
from time import sleep
import os

from elements.core import make_request
from elements.sessions.utilities import start_session, load_session
from elements.messages.utilities import send_direct_message

from elements.testing.utilities import enable_test_data, delete_test_data

class TestAPIRegistration(unittest.TestCase):
    pass
    #@classmethod
    #def setUpClass(cls):
    #    enable_test_data()
    #    # Start the test server
    #    cls.server = subprocess.Popen(['python', os.path.join('elements','testing','app.py')])
    #    sleep(0.5)

    #def test_register(self):
    #    body = {
    #        "content": "",
    #        "author": "new_person"
    #    }

    #    request = make_request('http://localhost:1618/register', body=body, method="POST")

    #@classmethod
    #def tearDownClass(cls):
    #    cls.server.kill()
    #    delete_test_data()
        
        

