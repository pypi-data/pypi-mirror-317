import json
import base64
import urllib

from elements.core import request, abort, make_request
from elements.notes import Note
from elements.sessions.utilities import session
from elements.accounts.utilities import lookup

# This is a function for making a request to a remote API, optionally
# using an authorization function to authenticate the identity of the
# individual making the request.

def auth_request(url, **kwargs):
    body = kwargs.get('body', {})
    method = kwargs.get('method', 'GET')
    authorization = kwargs.get('authorization', None)
    headers = kwargs.get('headers', {})
    s = kwargs.get('session', session())

    if authorization == 'Nostr':
        b64 = s.authorize(url, method)
        headers['Authorization'] = f'Nostr {b64}'

    if authorization == 'Solar':
        headers['Authorization'] = f'Solar {s.key}'

    kwargs['headers'] = headers
    return make_request(url, **kwargs)
    

# Request verification will block any requests which are not made with an
# appropriate Authorization header, and then return the account or profile
# associated with the request data.
def verify_request():
    auth = request.get_header('Authorization')
    if auth is None:
        abort(403, "No Authorization header provided")

    scheme, data = auth.split()
    if scheme == "Nostr":
        decoded = base64.b64decode(data)
        event = json.loads(decoded)
        note = Note.import_event(data=event)
        if not note.verified():
            abort(401, "Note verification failed")
            
        if not note.tags.get('u')[0] == request.url:
            abort(401, "Note verification failed")
            
        if not note.tags.get('method')[0].upper() == request.method:
            abort(401, "Note verification failed")

        author = lookup(note.pubkey)
        if author is None:
            abort(401, "No account found")

        return author

    elif scheme == "Solar":
        session = Sessions.all().get(data)
        if session is None:
            abort(400, "No session found")

        return session.member

    else:
        abort(403, f'Unable to verify {scheme} as Authorization header')
    
    
    
