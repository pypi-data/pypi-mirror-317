import re

from elements.core import request, response, redirect
from elements.posts import Post
from elements.sessions.utilities import session

def post(path="posts"):
    planet = request.route.config.get('planet', '')

    planets = request.route.config.get('planets')
    for mount_path in planets:
        if path.startswith(mount_path) and planetary is False:
            path = re.sub(fr'^{mount_path}', '', path)

            # We preserve this if needed for the redirect.
            planet = mount_path;

    s = session()
    if s is None:
        return redirect(path)

    member = s.member
    
    f = request.forms.decode('utf8')
    f['author'] = member.name
    p = Post(f)
    for key in request.files:
        upload = request.files[key]
        if upload.filename != "empty":
            p.attach(upload)

    path = p.save(path=f"posts/{member.name}")
    path = p.path.url
    if planet != '':
        path = f'/{planet}/{path}/'
    else:
        path = f'/{path}/'
        
    return redirect(path)
