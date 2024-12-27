import os, re

from elements.core import request, response, error, redirect, Element, Timestamp
from elements.sessions.utilities import session, start_session, load_session, end_session, auth_session
from elements.accounts import Accounts
from elements.accounts.integrations import Nostr

### DEPRECATION NOTICE ###
# This element is being superceded by 'actions'

'''

API

The Abstract Programming Interface, or API for short, defines
a number of functions which are used to implement common
patterns within interactive webpages: logging in and out,
making a post, editing your profile, checking a notification etc.

'''

def login(*args, **kwargs):

    if request.method != "POST":
        # The 'keyed' login flow is the only valid reason for a "GET" request.
        # If the key matches the "auth" value of an existing account, they
        # will be logged in and authorized automatically.

        redirect_url = '/'

        key = request.query.get('key')
        if key is None:
            raise ValueError("invalid login request")

        auth = None

        for account in Accounts.all():
            seed = account.data.content.get('seed')
            if key == seed:
                auth = account.data.content.get('auth')

        if auth:
            nsec = Nostr(auth).nsec
            s = auth_session(nsec)

        else:
            # registering new account
            redirect(f'/register/?key={key}')

        response.set_cookie('session', nsec, path="/", maxage=60*60*24*52)

        response_format = request.headers.get('Accept')
        if response_format == "text/plain":
            return session_key
        else:
            return redirect(redirect_url)

    elif request.method == "POST":
        f = request.forms
        name = f.getunicode('name').lower()
        password = f.getunicode('password')

        referrer = request.environ.get('HTTP_REFERER')
        redirect_url = f.getunicode('redirect') or referrer

        remember = f.getunicode('persistent')
        if remember == "on":
            persistent = True
        else:
            persistent = False

        session_key = start_session(name, password, persistent=persistent)
        if session_key is None:
            return redirect(referrer)

        response.set_cookie('session', session_key, path="/", maxage=60*60*24*52) # One year

        response_format = request.headers.get('Accept')
        if response_format == "text/plain":
            return session_key
        else:
            return redirect(redirect_url)

def logout(*args, **kwargs):
    key = request.get_cookie('session')
    end_session(key)
    response.delete_cookie('session', path="/")
    return redirect(request.environ.get("HTTP_REFERER"))

# This is a basic, extendable implementation
# It uses a basic Create, Read, Update, Delete structure.
def endpoint(path = "", element=Element, auth=False, **kwargs):
    planetary = kwargs.get('planetary', False)
    attach_media = kwargs.get('attach_media', False)
    planet = ''

    # If a request is made to a specific planet and we don't
    # want a planetary request (one that is not universal to
    # the entire Solar system) we remove the beginning of the
    # path so that it resolves properly in the data directory
    planets = request.route.config.get('planets')
    for mount_path in planets:
        if path.startswith(mount_path) and planetary is False:
            path = re.sub(fr'^{mount_path}', '', path)

            # We preserve this if needed for the redirect.
            planet = mount_path;

    # Set default redirect path.
    redirect_path = request.environ.get('HTTP_REFERER')

    # Change the path into something that the storage
    # module can work with
    path = path.strip('/')

    # TODO: Add verification
    if auth:
        pass

    # Get the member from the session.
    # (should be taken care of with auth)
    s = session()
    if s is None:
        return redirect(redirect_path)
    else:
        member = s.member


    # If we are working with a complex object, we may
    # only want to work with a section of it.
    at = request.query.get('at')

    # HTML forms only support post, so we pass the method in the
    # query string if we want to do something else.
    if request.method == "POST":
        method = request.query.get('method', request.method).upper()
    else:
        method = request.method

    # Branch based on request method.
    if method == "POST":
        # Create
        data = { **request.forms, 'author': member }
        e = element(**data)

        if attach_media:
            for key in request.files:
                upload = request.files[key]
                if upload.filename != "empty":
                    e.attach(upload)

        # In the case of a comment (possibly other elements as well), we want 
        # to make sure that the element is still saved in its appropriate
        # directory by default.
        if not path.startswith(e.directory):
            path = os.path.join(e.directory, path)

        e.save(path=path)

    elif method == "GET":
        # Read an existing element
        e = element.load(path)
        if e is None:
            return error(404)
        else:
            return e.flatten()

    elif method == "PUT":
        # Update an existing element
        e = element.load(path)
        data = { **request.forms.decode('utf8') }

        # If we've passed "at", work with a specific
        # component of a compound.
        if at:
            e = getattr(e, at)

        if isinstance(e.content, dict):
            # If we have a dictionary here,
            # we update it with new values
            e.content.update(data)
        else:
            # Otherwise, Set the content.
            e.content = data.get('content') or e.content

        e.ts = Timestamp()
        e.save()

    elif method == "DELETE":
        # Delete
        if not path.startswith(element.directory):
            path = os.path.join(element.directory, path)

        e = element.load(path)
        if e:
            e.unsave()

        # Redirect to the parent dir
        redirect_path = os.path.join(planet, e.directory, "")


    # Response Finalization:
    # If the response has an 'Accept application/json'
    # header, we return the object directly.

    response_format = request.headers.get('Accept')
    if response_format == "application/json":
        return e.flatten()

    # Otherwise, we return a redirect to the object's view
    else:
        return redirect(redirect_path)
