import os, re

from elements.core import request, error, redirect, Element, Timestamp
from elements.sessions.utilities import session

# This is a basic, extendable action endpoint 
# It implements a Create, Read, Update, Delete interface.
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
