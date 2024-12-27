from elements.core import Bottle, chevron_template, Element, Collection
from elements.api import endpoint, login, logout
from elements.api.accounts import nostr, register
from elements.api.messages import conversation
from elements.testing.utilities import enable_test_data

import os

##################################################
### Planet Data ##################################
##################################################

app = Bottle()
path = '/'

def defaults(additional_data=None):
    default_data = {
            'title': 'New',
            'path': path,
            'static': path + 'static/'
    }

    # if there's extra data, (over)write it to the default info.
    if additional_data is not None:
        for key, value in additional_data.items():
            default_data[key] = value

    return {
            # This is the path from the Solar root directory
            'partials_path': f'views/components/',

            # This is the filetype we use for components
            'partials_ext': 'mo',

            # This is the data that gets rendered into the template
            'data': default_data
    }

##################################################
### API Section ##################################
##################################################

# we register certain paths to preconfigured endpoints
# for use within the application
app.endpoint('element', endpoint)
app.post('/login', callback=login)
app.get('/logout', callback=logout)
app.get('/.well-known/nostr.json', callback=nostr)
app.post('/register', callback=register)
app.post('/<path:path>/conversation', callback=conversation)

##################################################
### Frontend Routes ##############################
##################################################

# These are the routes that expect to render content for the client

@app.route('/<element_name>/')
def el(element_name):
    element = Element.load(element_name)
    data = {
        'element': element
    }
    return chevron_template(f'test_single.html', **defaults(data));

@app.route('/')
def index():
    elements = Collection.load('', recursive=False)
    data = {
        'elements': elements.contents
    }
    return chevron_template(f'test.html', **defaults(data));


##################################################
### Running the code #############################
##################################################

# Normally, a planet will be pushed into orbit by the main app within the Solar system.
# However, any app can serve as the main landing page if given access to elements

if __name__ == "__main__": 
    enable_test_data()
    app.run(host='0.0.0.0', port=1618, debug=True)
