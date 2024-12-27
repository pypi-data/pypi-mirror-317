import os
import shutil

from elements.core import Config
from elements.sessions import Sessions
from elements.accounts import Accounts

def enable_test_data():
    directory = "test_data"
    c = Config.load()
    c.override('data_folder', directory)
    c.override('host', 'localhost:0')
    c.override('base', os.path.join(directory, ""))
    Sessions.all(reload=True)
    Accounts.all(reload=True)

def delete_test_data():
    try:
        shutil.rmtree('test_data/')
    except FileNotFoundError:
        pass
