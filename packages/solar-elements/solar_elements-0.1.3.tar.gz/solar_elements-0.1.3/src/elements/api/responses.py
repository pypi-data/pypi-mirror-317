import re
import os

from elements.core import request, Element
from elements.responses import Response, Responses
from elements.bookings import Bookings
from elements.sessions.utilities import session
from elements.api import endpoint

def rsvp(path):
    s = session()

    planets = request.route.config.get('planets')
    for mount_path in planets:
        if path.startswith(mount_path):
            path = re.sub(fr'^{mount_path}', '', path)

    # This is janky. I'm letting it slide for now, but there
    # should be a 1:1 correspondence between path and note
    # at all times. Convenience functions should redirect,
    # e.g. /account/ -> /members/npc/edit

    # Rename 'bookings' to 'events', or override with a
    # different directory.
    path = path.strip('/')
    b = Bookings.all()
    e = b.find(path.split('/')[-1])
    
    r = Response.new(target=e, author=s.member, content="rsvp")
    r.save()

def unrsvp(path):
    s = session()
    planets = request.route.config.get('planets')
    for mount_path in planets:
        if path.startswith(mount_path):
            path = re.sub(fr'^{mount_path}', '', path)

    path = path.strip('/')
    print('b', os.path.join('responses', path, s.member.name))
    r = Response.load(os.path.join('responses', path, s.member.name))
    r.unsave()
    #b = Bookings.all()
    #e = b.find(path.split('/')[-1])

    #r = Responses.all()
    #responses = r.find(e.path, "target")
    #for response in response:
    #    if response.source.author == s.member.name:
    #        response.unsave()
