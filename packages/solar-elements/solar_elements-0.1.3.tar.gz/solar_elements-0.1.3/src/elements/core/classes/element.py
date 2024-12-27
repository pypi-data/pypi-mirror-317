from collections import defaultdict
from collections.abc import Iterable
from math import ceil
import json
import os.path
#from pathlib import Path
import glob
from elements.core.storage import SolarPath, save_file, load_file, delete, identify

from .timestamp import Timestamp
from .tagdict import TagDict

from elements.core.config import Config

c = Config.load()

'''

Element is the base class that all other components in the Solar System
are based on. It implements a standard constructor, along with basic
functions for loading and saving the element from storage. 

This class should generally not be used directly in any application.
It is intended as an abstract class to be inherited by other elements.

'''

# ### Element ###

# When any Element is created, it is passed a dictionary of values
# that define the object. This dictionary may or may not contain
# entries for the five basic values (content, author, created_at, kind,
# tags) along with any other number of tagged values which indicate extra
# details about the Element.

# ### Content ###
# The 'content' of an element is the basis of what it displays on the page.
# It can either be a plaintext value (e.g. Comment) or a dictionary (e.g.
# Profile). In some cases (e.g Post), the plaintext value is expected to 
# be processed before being sent to the templating engine.

# Content _must_ be a json serializable value by default.

# ### Pubkey ###
# The 'pubkey' of an element is a unique string identifier for the member 
# responsible for creating the element. When an element is loaded from 
# data, most constructors will look up the pubkey from Members and 
# attach it to the element as an attribute.

# ### Created At ###
# The created_at value is a timestamp of the exact moment an Element
# is (or was) instanced. This value is passed into a Timestamp and 
# saved to the element as 'ts' so that it can be operated on more easily.

# ### Kind ###
# The kind of an Element is its reference in the nostr ecosystem. A goal
# of Solar is to maintain full cross-compatibility with nostr, and every
# element with a kind other than -1 can be shared over relays.

class Element:
    kind = None
    directory = c.data_folder
    key_data = ['content', 'pubkey', 'created_at', 'kind', 'tags', 'filepath']

    def __init__(self, **data):
        if isinstance(data, list):
            raise ValueError('cannot create an element from a directory - use a Collection')

        self.content = data.get('content', "")
        self.pubkey = data.get('pubkey', bytes(32).hex())
        self.created_at = Timestamp(data.get('created_at'))
        self.tags = TagDict(data.get('tags', []))
        self.kind = data.get('kind', self.kind)

        # The path is location where the element can be found on the
        # filesystem. If the element does not exist on disk, this
        # value will be None.
        path = data.get('filepath')
        if path:
            self.path = SolarPath.to(path)
        else:
            self.path = None

        # We assert that this element is not part of a collection,
        # So that it has nothing to update when it saves
        self.collection = None

        for key in data:
            # If the data's key is in the key_data list, keep it there.
            if key in self.key_data:
                continue

            # For each remaining key in the data, we add it to
            # the element as a tag.
            else:
                value = data[key]
                if isinstance(value, list):
                    self.tags.append(key, value)
                else:
                    self.tags.append(key, [value])

    # By default, an Element will place any non-key data into the tags.
    # Using this constructor places it into the content dict instead.
    @classmethod
    def content_dict(cls, **data):
        content = data.get('content', {})
        if not isinstance(content, dict):
            raise ValueError("content must be a dictionary")

        for key in data:
            # If the data's key is in the key_data list, keep it there.
            if key in cls.key_data:
                continue

            # For each remaining key in the data, we add it to
            # a content dictionary
            else:
                content[key] = data[key]
        
        # Keep the content from being duplicated into the tags
        for key in content:
            del data[key]

        data['content'] = content
        return cls(**data)

    @classmethod
    def load(cls, path):
        data = load_file(path)

        # Data may return [] if it finds nothing, which
        # is a falsy value. If so, we return None.
        if data:
            e = cls(**data)
            e.path = SolarPath.to(path)
        else:
            return None

        return e

    # The 'save' function determines how the element will write to
    # disk. kwargs are passable, defaulting to the following values:

    # 'path'        -> The default directory for a given Element
    # 'overwrite'   -> True (replace file instead of making a new one)
    # 'name'        -> 'd' tag or first 8 characters of object id
    
    def save(self, **kwargs):
        if self.path:
            default_path = self.path.parent
        else:
            default_path = SolarPath.to(self.directory, dir=True)


        kwargs['path'] = kwargs.get('path', default_path)
        kwargs['overwrite'] = kwargs.get('overwrite', True)
        kwargs['name'] = kwargs.get('name', self.name)
        update = kwargs.pop('update', True)

        self.path = save_file(self.flatten(), **kwargs)

        # If the element is part of a collection, make sure
        # that collection is updated on the changes.
        if self.collection and update:
            self.collection.update()

        return self.path

    def unsave(self):
        path = self.path
        if path:
            delete(self.path)
            self.path = None

        # If the element is part of a collection, make sure
        # that collection is updated on the changes.
        if self.collection:
            updates = self.collection.update()

        return path

    def flatten(self, *args):
        representation = {
            'content': self.content,
            'pubkey': self.pubkey,
            'kind': self.kind,
            'created_at': int(self.created_at),
            'tags': self.tags.flatten()
        }
    
        return representation

    @property
    def hours(self):
        return self.tags.getfirst('hours')

    @property
    def name(self):
        if self.path:
            return self.path.stem
        else:
            return self.tags.getfirst('d')

    @property
    def meta(self):
        return { key: tags[key] for key in tags }

    # DEPRECATED IN FAVOR OF URL()
    # The 'clean path' is the path of the saved element relative to the data folder,
    # excluding the file suffix. This is mainly used for building URLs
    @property
    def clean_path(self):
        if self.path:
            clean = self.path.parent.relative_to(c.data_folder) / self.path.stem
            return clean.as_posix()
        else:
            return None

    # The path used to address this element within a URL
    @property
    def url(self):
        base = self.path
        if base:
            return base.url + '/'

    # This computes the id of the element
    @property
    def id(self):
        serialized = [0,self.pubkey,int(self.created_at),self.kind,self.tags.flatten(),self.content]
        return identify(serialized)

    @property
    def address(self):
        if self.pubkey is None or self.pubkey == bytes(32).hex():
            pubkey = ""
        else:
            pubkey = self.pubkey
        return f'{self.kind or ""}:{pubkey}:{self.name or ""}'


    # This function defines how the Element acts as a string
    def __str__(self):
        if isinstance(self.content, dict):
            return json.dumps(self.content)
        return self.content

    # This function indicates how Element is represented interactively
    def __repr__(self):
        key = self.id
        
        #return f'{type(self).__name__} - {key[:4]}..{key[-4:]}'
        return f'{type(self).__name__} - {key}'
