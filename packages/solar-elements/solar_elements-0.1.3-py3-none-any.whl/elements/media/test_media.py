import unittest
import os
import hashlib
from elements.media import Media, Picture
from elements.core import delete, FileUpload

from elements.testing.utilities import enable_test_data, delete_test_data

class TestMedia(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        enable_test_data()
        with open('testfile.txt', 'wb') as file:
            file.write(b'This is a test file, the contents are irrelevant.')

    def test_new_media(self):
        file = open('testfile.txt', 'rb')
        m = Media.new(file)
        m.save()
        file.close()
        self.assertTrue(m.tags.getfirst('url') != None)
        self.assertTrue(m.tags.getfirst('url').startswith('http://localhost:0/static/uploads/npc/'))
        m.unsave()

    def test_from_file_upload(self):
        with open('static/images/banner.jpg', 'rb') as f:
            upload = FileUpload(f, name="banner", filename="banner.jpg")
            m = Picture.new(upload.file)
            m.save()

    def test_load_media(self):
        m = Media.from_local('testfile.txt')
        path = m.save()
        self.assertTrue(m.tags.get('url') != None)
        m2 = Media.load(path)
        self.assertEqual(m.id, m2.id)

    def test_image_resize(self):
        m = Picture.from_local('static/images/banner.jpg', {"author": "npc"})
        thumb = m.thumbnail()
        path = m.save()
        # Once we save the media element, the file is closed to further operations.
        with self.assertRaises(ValueError) as cm:
            thumb = m.thumbnail()

        m2 = Picture.load(path)
        self.assertEqual(m.id, m2.id)

        with open('static/images/banner.jpg', 'rb') as f:
            fbytes = f.read()
            original_size = len(fbytes)
            sha256 = hashlib.sha256(fbytes).hexdigest()

        ox = m2.tags.get('ox')[0]
        self.assertEqual(ox, sha256)

        saved_size = m2.tags.get('size')[0]
        self.assertTrue(saved_size < original_size)

        self.assertTrue(m2.tags.get('url') != None)
        #print('url', m2.tags.get('url'))
            
    @classmethod
    def tearDownClass(cls):
        os.remove('testfile.txt')
        delete_test_data()

