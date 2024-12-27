import json
from elements.core import request, response

# This is a janky plugin - rewrite when possible

class FlashPlugin(object):
    name = 'flash'

    def __init__(self, key='flash', secret=None):
        self.key = key
        self.secret = secret
        self.app = None

    def setup(self, app):
        self.app = app
        self.app.add_hook('before_request', self.load_flashed)
        self.app.add_hook('after_request', self.set_flashed)
        self.app.flash = self.flash
        self.app.get_flashed_messages = self.get_flashed_messages

    def load_flashed(self):
        m = request.get_cookie(self.key, secret=self.secret)
        if m is not None:
            response.flash_messages = json.loads(m)

    def set_flashed(self):
        if hasattr(response, 'flash_messages'):
            response.set_cookie(self.key, json.dumps(response.flash_messages), secret=self.secret, path="/")
            m = request.get_cookie(self.key, secret=self.secret)
            delattr(response, 'flash_messages')

    def flash(self, message, level=None):
        if not hasattr(response, 'flash_messages'):
            response.flash_messages = []
        response.flash_messages.append({'message': message, 'type': level})

        # So... this doesn't really work properly unless
        # I set this cookie here. I really am not sure
        # why. It would be good to rewrite this plugin
        # to make it more usable.
        response.set_cookie('solar', '')

    def get_flashed_messages(self):
        if hasattr(response, 'flash_messages'):
            m = response.flash_messages
            delattr(response, 'flash_messages')
            response.delete_cookie(self.key, path="/")
            return m
            
    def apply(self, callback, context):
        return callback
