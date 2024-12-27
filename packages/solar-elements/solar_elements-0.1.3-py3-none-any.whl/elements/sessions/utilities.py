from elements.core import request, response
from elements.sessions import Session, Sessions
from elements.accounts import Accounts
from elements.notifications import Notifications
from elements.accounts.integrations import Nostr
#from elements.messages import Conversations

# These utilities are intended to simplify the management
# of sessions in the Solar system. Sessions is not concerned
# with managing the global members object, so we take care
# of member lookup here.

# session() returns the session attached to
# a given request's session key, if it exists.
def session(*args, **kwargs):
    key = request.get_cookie('session')

    if key is None:
        return None
    elif key.startswith('nsec'):
        # A 'nsec' key implies direct login, and will start
        # new session or attach to an existing one.
        s = auth_session(key)
    else:
        s = load_session(key)

    # Clear the cookie if it isn't attached to
    # an active session.
    if s is None:
        response.delete_cookie('session', path="/")
        return None

    s.notifications = Notifications.load(s.member.name)
    #s.conversations = Conversations.load(s)
    return s

def auth_session(nsec) -> Session:
    sessions = Sessions.all()
    accounts = Accounts.all()

    s = Sessions.all().find(nsec)

    if s is None:
        nostr = Nostr.from_nsec(nsec)
        account = accounts.find(nostr.public_key.hex())
        if account is None:
            return None

        # The private_key acts as a 'secondary password' for NPC accounts
        s = sessions.new(account, nostr.private_key.hex(), key=nsec)

    return s


def start_session(name, password, persistent=False):
    sessions = Sessions.all()
    accounts = Accounts.all()
    account = accounts.find(name)

    try:
        app = request.app
    except RuntimeError:
        app = None

    if account is None:
        if app:
            app.flash(f'Member "{name}" not found', "error")
        return None

    try:
        if persistent and account.kind == "npc":
            session = sessions.auth(account, password)
        else:
            session = sessions.new(account, password, persistent=persistent)
    except (ValueError, AssertionError):
        if app:
            app.flash(f'Incorrect password for "{name}"', "error")
        return None

    #session.notifications = Notifications.load(name)
    #session.conversations = Conversations.load(session)

    return session.key

def load_session(key):
    s = Sessions.all().find(key)
    if s is None:
        return None

    #s.member = Accounts.all().find(s.account.name)
    s.member.update()
    #s.notifications.update()
    return s

def end_session(key):
    return Sessions.all().delete(key)
