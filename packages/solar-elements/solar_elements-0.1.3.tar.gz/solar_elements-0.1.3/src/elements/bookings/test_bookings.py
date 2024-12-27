import unittest

from elements.accounts import NPC
from elements.notes import Note, Notes
from elements.core import Timestamp
from elements.places import Place
from elements.bookings import Booking, Bookings
from elements.testing.utilities import enable_test_data, delete_test_data


class TestBookings(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        enable_test_data()
        cls.m = NPC.register(name="test", master_key=bytes(32))
        cls.p = Place.new(name="Cafe")
        cls.p.save()
        cls.m.save()

    def test_booking(self):
        t = Timestamp()
        t_1 = t.replace(day=5, hour=10, minute=30)
        t_2 = t.replace(day=5, hour=12, minute=30)
        t_3 = t.replace(day=5, hour=13, minute=30)

        b = Booking.new(content="# Hello", title="Event Title", location="cafe", start = int(t_1), end = int(t_2))
        self.assertTrue(b.name.startswith('event-title-cafe'))

        with self.assertRaises(ValueError) as cm:
            b2 = Booking.new(start = int(t_1), end = int(t_2), location="cafe")

        # Conflicts return the conflicting event in the args
        conflict = cm.exception.args[1]
        self.assertEqual(conflict.id, b.id)

        # Back-to-back events are not a problem
        b3 = Booking.new(content="# Hello", title="Event Title", location="cafe", start = int(t_2), end = int(t_3))
        self.assertTrue(b.meta.get('title') == b3.meta.get('title'))
        self.assertTrue(b.name != b3.name)

    def test_rescheduling(self):
        t = Timestamp()
        t_1 = t.replace(day=9, hour=10, minute=30)
        t_2 = t.replace(day=9, hour=12, minute=30)
        t_3 = t.replace(day=9, hour=13, minute=30)

        b = Booking.new(content="# Hello", title="Event Title", location="cafe", start = int(t_1), end = int(t_2))
        b.reschedule(days=1)
        self.assertEqual(b.start.day, 10)

        b2 = Booking.new(content="# Hello", title="Event Title", location="cafe", start = int(t_1), end = int(t_2))
        with self.assertRaises(ValueError) as cm:
            b.reschedule(days=-1)

        conflict = cm.exception.args[1]
        self.assertEqual(conflict.id, b2.id)

    def test_duplication(self):
        t = Timestamp()
        t_1 = t.replace(day=12, hour=10, minute=30)
        t_2 = t.replace(day=12, hour=12, minute=30)
        t_3 = t.replace(day=12, hour=13, minute=30)

        b = Booking.new(content="# Hello", title="Event Title", location="cafe", start = int(t_1), end = int(t_2))
        b2 = b.duplicate()
        self.assertEqual((b2.start - b.start).days, 7)
        b3 = b.duplicate(days=2)
        self.assertEqual((b3.start - b.start).days, 2)

    def test_bookings(self):
        t = Timestamp()

        # Two times, one hour apart.
        t_1 = t.replace(day=11, hour=11, minute=30)
        t_2 = t.replace(day=11, hour=12, minute=30)

        bl = Bookings.all()
        b = Booking.new(content="# Hello", title="Event Title", location="cafe", start = int(t_1), end = int(t_2))
        search_day = b.days[0]
        found = bl.find(search_day, 'day')[0]
        self.assertEqual(found.id, b.id)

        found.reschedule(weeks=1)

        successful_search =  bl.find(found.days[0], 'day')
        unsuccessful_search  =  bl.find(search_day, 'day')

        self.assertEqual(len(successful_search), 1)
        self.assertEqual(len(unsuccessful_search), 0)

    @classmethod
    def tearDownClass(cls):
        delete_test_data()
