from elements.core import request, response, redirect, Element
from elements.core.storage import clean
from elements.sessions.utilities import session

def edit(path):
    s = session()
    if s is None:
        return redirect(path)

    member = s.member

    # 'path' is greedy, so we make sure
    # that the edge slashes are dropped.
    path = path.strip('/')
    
    p = Element.load(path)

    f = request.forms.decode('utf8')

    # Only updates content dicts for now
    if isinstance(p.content, dict):
        p.content.update(f)

    # This needs to be less generic, it doesn't
    # work for editing an account because it saves
    # as an element, obviously
    #path = p.save()
    return redirect(f'/{clean(path)}/')
