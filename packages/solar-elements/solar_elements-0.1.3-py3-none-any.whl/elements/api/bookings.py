import re

from elements.core import request
from elements.bookings import Booking
from elements.api import endpoint

def booking(path):
    return endpoint(path, element=Booking, auth=False, attach_media=True)

def duplicate(path, element=Booking):
    planets = request.route.config.get('planets')
    for mount_path in planets:
        if path.startswith(mount_path) and planetary is False:
            path = re.sub(fr'^{mount_path}', '', path)

    path = path.strip('/')
    b = element.load(path)
    b2 = b.duplicate()
    return b2.clean_path
