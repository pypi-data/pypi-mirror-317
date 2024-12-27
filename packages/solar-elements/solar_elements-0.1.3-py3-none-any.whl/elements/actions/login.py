import os, re

from elements.core import request, response, redirect
from elements.sessions.utilities import start_session, auth_session
from elements.accounts import Accounts
from elements.accounts.integrations import Nostr

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

