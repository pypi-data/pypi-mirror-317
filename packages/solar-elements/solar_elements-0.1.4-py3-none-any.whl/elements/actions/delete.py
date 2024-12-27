from elements.core import Element, abort
from elements.sessions.utilities import session

# This may need to be extended to delete collections (e.g. Accounts)

def delete(*args, **kwargs):
    s = session()
    if s is None:
        return abort(401)

    if len(args) == 0:
        return abort(400)

    element = args[0]
    element.unsave()


