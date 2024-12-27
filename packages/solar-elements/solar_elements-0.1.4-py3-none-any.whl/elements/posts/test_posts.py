import unittest
from elements.core import FileUpload
from elements.posts import Post, Posts
from elements.testing.utilities import enable_test_data, delete_test_data

TEST_MD = '# Heading \n\n paragraph text'
TEST_MD2 = '# New Heading \n\n more paragraph text'
TEST_HTML = '''<h1>Heading</h1>
<p>paragraph text</p>'''

# This value represents a defused XSS attack.
TEST_XSS = "<p>&lt;button onclick='injectPayload()'/&gt;</p>"

class TestPosts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        enable_test_data()

    def setUp(self):
        self.p = Post(**{ 'content': TEST_MD, 'd': 'post-title'})
        self.p2 = Post(**{ 'content': TEST_MD2, 'd': 'post-title2'})
        self.p3 = Post(**{ 'content': TEST_MD2, 'd': 'post-title3'})

        self.p.save()
        self.p2.save()
        self.p3.save()

    def test_post_generation(self):
        self.assertEqual(self.p.name, 'post-title')
        self.assertEqual(self.p.html, '''<h1>Heading</h1>
<p>paragraph text</p>''')
        self.assertEqual(len(self.p.tags.get('published_at')), 1)

    def test_image_attachment(self):
        with open('static/images/banner.jpg', 'rb') as f:
            upload = FileUpload(f, name="image", filename="banner.jpg")
            self.p.attach(upload)

        self.assertTrue(len(self.p.tags.get('media')) == 1)
        self.assertTrue(self.p.media.get('banner') is not None)

    def test_saving_and_loading(self):
        path = self.p.save()
        loaded = Post.load(path)
        self.assertEqual(self.p.id, loaded.id)
        self.p.unsave()

    def test_media_persistence(self):
        with open('static/images/banner.jpg', 'rb') as f:
            upload = FileUpload(f, name="image", filename="banner.jpg")
            self.p.attach(upload)

        path = self.p.save()
        loaded = Post.load(path)
        self.assertEqual(len(self.p.media), len(loaded.media))

    def test_sanitation(self):
        self.p.content = "<button onclick='injectPayload()'/>"
        self.assertEqual(self.p.html, TEST_XSS)

    def test_editing(self):
        id1 = self.p.id
        pub = self.p.tags.get('published_at')[0]
        self.p.content = TEST_MD2
        path = self.p.save()
        loaded = Post.load(path)
        self.assertNotEqual(TEST_HTML, loaded.html)
        self.assertNotEqual(id1, loaded.id)
        self.assertEqual(loaded.tags.get('published_at')[0], pub)

    def test_pagination(self):
        pl = Posts.load('posts')

        pl.page_size = 1
        page_1 = pl.page(0)
        page_2 = pl.page(1)
        self.assertEqual(page_1[0].id, self.p.id)
        self.assertEqual(page_2[0].id, self.p2.id)

        pl.page_size = 10
        big_page1 = pl.page(0)
        big_page2 = pl.page(1)

        self.assertEqual(len(big_page1), 3)
        self.assertEqual(len(big_page2), 0)

    def test_author_lookup(self):
        pl = Posts.load('posts')
        from_test = pl.by_author('npc')
        self.assertEqual(len(from_test), 3)
        self.assertEqual(from_test[0].name, 'post-title3')

    def tearDown(self):
        self.p.unsave()
        self.p2.unsave()
        self.p3.unsave()
        
    @classmethod
    def tearDownClass(cls):
        delete_test_data()

