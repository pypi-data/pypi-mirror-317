from datetime import timedelta
from calendar import monthrange

from elements.core import Element, Timestamp
from elements.core.storage import slugify
from elements.posts import Post, Posts
from elements.places import Place, Places

'''
             _____________          
            |             |          
            |  June 2024  |      
            |_____________|          
            |_|_|_|_|_|_|_|          
            |_|_|_|_|X|_|_|          
            |_|_|_|_|_|_|_|          
            |_|_|_|_|_|_|_|          
                                             
               Bookings

The Booking element is used to reserve a space
for a specific amount of time.

Booking events are organized by the day(s) they
occur and the spaces where they happen. When 
making a new booking, we first check for any 
conflicts in the same location.

Booking builds on the Post element, adding
tooling to edit, duplicate and reschedule events. 
'''

class Booking(Post):
    directory = 'bookings'
    kind = 31923

    @classmethod
    def new(cls, **data):
        bookings = Bookings.all()
        booking = cls(**data)
        if booking.start is None:
            raise ValueError('No start timestamp provided')

        if booking.end is None:
            raise ValueError('No end timestamp provided')

        if booking.start > booking.end:
            raise ValueError('End time before start time')

        booking.save()
        bookings.add(booking)
        return booking

    def validate(self):
        bookings = Bookings.all()

        # Check for conflicts between bookings on the same day(s)
        for day in self.days:
            existing_bookings = bookings.find(day, 'day')

            if existing_bookings is None:
                continue

            # Wrap it in a list to be iterable
            if not isinstance(existing_bookings, list):
                existing_bookings = [existing_bookings]

            for b in existing_bookings:
                if b is None or b.location != self.location:
                    continue

                if  b.start <= self.start < b.end:
                    raise ValueError('Booking overlaps with ' + str(b.path), b)
                elif  b.start < self.end <= b.end:
                    raise ValueError('Booking overlaps with ' + b.path, b)


    # Validate the booking before we save it!
    def save(self, **kwargs):
       self.validate()
       return Post.save(self, **kwargs)

    # We overwrite the Post's name property to append the booking's date
    @property
    def name(self):
        title = self.tags.getfirst('title')
        start = int(self.start)
        location = self.location
        if title and location:
            return f'{slugify(title)}-{location.name}-{start}'
        elif title:
            return f'{slugify(title)}-{start}'
        else:
            return super().name

    @property
    def location(self):
        name = self.tags.getfirst('location')
        if name is None:
            return None

        place = Places.all().find(name)
        return place or None

    @property
    def start(self):
        tag = self.tags.getfirst('start')
        if tag is None:
            return None

        return Timestamp(tag)

    @property
    def end(self):
        tag = self.tags.getfirst('end')
        if tag is None:
            return None

        return Timestamp(tag)

    @property
    def days(self):
        day_list = []
        for i in range((self.end - self.start).days + 1):
            day = self.start + timedelta(days=i)
            day_list.append(day.strftime('%Y-%m-%d'))

        return day_list

    @property
    def price(self):
        value = self.tags.getfirst('price')
        cost = self.tags.getfirst('cost')

        if value == "free":
            return "free"
        elif value == "pwyc":
            return f"PWYC (suggested ${cost})"
        elif value == "paid":
            return cost
            

    # Reschedule accepts the parameters of a timedelta
    # and applies them to the start and end
    def reschedule(self, target='both', **options):
        self.unsave()
        delta = timedelta(**options)

        if target == 'start' or target == 'both':
            start = self.start + delta
            self.tags.replace('start', [int(start)])

        if target == 'end' or target == 'both':
            end = self.end + delta
            self.tags.replace('end', [int(end)])

        # TODO: find out why this doesn't resave in the same folder?
        # originals are under 'admin', for some reason
        self.save()

    # By default, duplicate creates a new event one week from the day.
    # It can be passed any of the same options as reschedule.
    def duplicate(self, **options):
        if len(options) == 0:
            options['weeks'] = 1

        cls = type(self)
        dupe = cls(**self.flatten())
        dupe.reschedule(**options)
        return dupe

class Bookings(Posts):
    default_class = Booking
    directory = 'bookings'

    class_map = {
        Booking.kind: Booking
    }

    buckets = { **Posts.buckets, 'day': lambda e: e.days, 'location': lambda e: e.location }


    # TODO options will be used to specify filters
    def upcoming(self, limit=None, **options):
        now = Timestamp()
        results = []
        for booking in self.content:
            if booking is None:
                continue

            if booking.start > now:
                results.append(booking)

        results.sort(key=lambda e: e.start)

        if limit:
            return results[:limit]
        else:
            return results
                
        
    # TODO: This will be refactored to work with HTMX

    # Render returns a dictionary built for rendering
    # in a month-to-month display
    def render(self, **options):
        # Number of upcoming events to set aside
        upcoming = options.get('upcoming') or 5

        now = Timestamp()

        calendar_data = { 'upcoming': [] }
        for booking in self.content:

            # Skip any recently deleted bookings
            if booking is None:
                continue

            m = booking.start.month
            y = booking.start.year
            d = booking.start.day - 1 # Zero-indexing


            # Record how long the event goes for
            diff = booking.end - booking.start

            key = f'{m}{y}'
            if calendar_data.get(key) is None:
                _, days = monthrange(y, m)
                calendar_data[key] = [None] * days

            data = booking.meta
            data['name'] = booking.name
            if booking.location:
                data['location'] = booking.location.display_name
            else:
                data['location'] = ""

            # We iterate over all the days of the event
            for i in range(diff.days) or range(1):
                day = d + i
                if calendar_data[key][day] is None:
                    calendar_data[key][day] = [data]
                else:
                    calendar_data[key][day].append(data)

            # Manage the 'upcoming' list
            if booking.start > now and len(calendar_data['upcoming']) < upcoming:
                calendar_data['upcoming'].append(data)

        return calendar_data
