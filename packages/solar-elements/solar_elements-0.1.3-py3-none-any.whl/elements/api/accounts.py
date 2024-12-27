from elements.core import request, response, redirect
from elements.accounts import NPC, Accounts
from elements.api import start_session, load_session

members = Accounts.all()

# /.well-known/solar.json
def profiles(*args, **kwargs):
    members.update()
    response.set_header('Content-Type', 'application/json')
    return members.dict()

# /.well-known/nostr.json
def nostr(*args, **kwargs):
    members.update()
    names = {}
    relays = {}

    for member in members.contents:
        if member.pubkey:
            names[member.name] = member.pubkey
            relays[member.pubkey] = ["nothing yet"]
        
    response.set_header('Content-Type', 'application/json')
    return { 'names': names, 'relays': relays, 'profiles': members.profiles_by_pubkey() }

# Registration receives 
def register(*args, **kwargs):
    redirect_path = request.environ.get('HTTP_REFERER')

    if request.method == "POST":
        f = request.forms

        # Not yet implemented
        registration_key = f.get('content')

        author = f.get('author')
        password=f.get('password') or author

        key = f.get('key')
        if key:
            m = NPC.register(name=author, role="member", password=password, master_key=bytes.fromhex(key))
        else:
            m = NPC.register(name=author, role="member", password=password)


        # Creating the profile
        def add_to_profile(key):
            value = f.getunicode(key)
            if value:
                m.profile.content[key] = value

        add_to_profile('bio')
        add_to_profile('email')
        add_to_profile('display_name')

        m.save()
        members.update()

        session_key = start_session(author, password)
        session = load_session(session_key)

        response.set_cookie('session', session_key, path="/")

    return redirect(redirect_path)
    


