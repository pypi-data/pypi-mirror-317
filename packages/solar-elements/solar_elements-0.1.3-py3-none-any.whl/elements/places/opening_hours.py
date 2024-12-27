# Basic implementation of OpenStreetMaps opening_hours spec.
# https://wiki.openstreetmap.org/wiki/Key:opening_hours/specification

from datetime import datetime
import time

DAYS = ["su", "mo", "tu", "we", "th", "fr", "sa", "ph"]
FULL_DAYS = [
    "Sunday", 
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Holidays"
]

class OpeningHours:
    def __init__(self, opening_hours_string):
        now = datetime.now()
        self.days = { k: (None, None) for k in DAYS }
        for entry in opening_hours_string.split(';'):
            entry = entry.strip() # Clean whitespace

            # This entry applies to all days
            if entry.find(' ') == -1:
                days = None
                hours = entry
            else:
                days, hours = entry.split(' ')

            if hours == "closed" or hours == "off":
                dt_open = None
                dt_close = None
            else:
                opening, closing = hours.split('-')

                open_h, open_m = opening.split(':')
                dt_open = now.replace(hour=int(open_h), minute = int(open_m))

                close_h, close_m = closing.split(':')
                dt_close = now.replace(hour=int(close_h), minute = int(close_m))

            # Set all days
            if days is None:
                self.days = { k: (dt_open, dt_close) for k in DAYS }
                continue
                

            for day in days.split(','):
                # If it's a range, set each day
                if "-" in days:
                    start, end = days.split('-')
                    s = DAYS.index(start.lower())
                    e = DAYS.index(end.lower())
                    for i in range(s, e+1):
                        self.days[DAYS[i]] = (dt_open, dt_close)
                else:
                    self.days[day.lower()] = (dt_open, dt_close)

    # This is mainly designed for rendering hours into a template
    @property
    def hours(self):
        l = []
        for i, day in enumerate(DAYS):
            try:
                start, end = self.days[day]
                if start is None:
                    continue

                s = start.strftime('%I:%M %p')
                e = end.strftime('%I:%M %p')

                l.append({
                    'day': FULL_DAYS[i],
                    'range': f'{s} - {e}'
                })

            except ValueError:
                continue

        return l


    @property
    def now(self):
        now = datetime.now()
        day = DAYS[now.weekday()]
        try:
            tm_open, tm_close = self.days[day]

        # Can't destructure? Definitely closed.
        except ValueError:
            return False

        return now > tm_open and now < tm_close
