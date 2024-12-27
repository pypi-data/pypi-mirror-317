import unittest
from elements.accounts import NPC, Accounts
from elements.posts import Post
from elements.jobs import Job, Jobs

from elements.testing.utilities import enable_test_data, delete_test_data

class TestJobs(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        enable_test_data()
        cls.m = NPC.register(name='test')
        cls.m.save()

        cls.j = Job(title="Job 1", author=cls.m)
        cls.j2 = Job(title="Job 2", author=cls.m)
        cls.j.save()
        cls.j2.save()

    def test_job(self):
        self.assertEqual(self.j.status, 'incomplete')
        self.j.complete()
        self.assertEqual(self.j.status, 'complete')

    def test_save_load(self):
        self.j.complete()
        path = self.j.save()
        j = Job.load(path)
        self.assertEqual(j.status, 'complete')

    def test_jobs(self):
        self.j.complete()
        self.j.save()
        jobs = Jobs.all()
        self.assertEqual(len(jobs.find('complete', 'status')), 1)
        self.assertEqual(len(jobs.find('incomplete', 'status')), 1)
        self.assertEqual(jobs.find('other', 'status'), None)

    @classmethod
    def tearDownClass(self):
        self.m.unsave()
        self.j.unsave()
        delete_test_data()
