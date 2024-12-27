from elements.core import request, response, redirect
from elements.sessions.utilities import end_session, auth_session

def logout(*args, **kwargs):
    key = request.get_cookie('session')
    end_session(key)
    response.delete_cookie('session', path="/")
    return redirect(request.environ.get("HTTP_REFERER"))
