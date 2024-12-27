from collections import defaultdict
from collections.abc import Iterable
from math import ceil
from elements.core.storage import SolarPath, load_file, load_directory
from elements.core.config import Config

from .element import Element
from .timestamp import Timestamp

c = Config.load()

# ### Collections ###

# A Collection is a list of Elements in the same directory.

# Collections are useful for being able to index loaded data with
# a given value, making it possible to look up entries in O(1) time
# once loaded to memory.

# Collections also allow for returning subsets of the data based on
# indexed information (e.g. the element's file path)

class Collection:
    default_class = Element
    directory = "collection"

    # The class map indicates the constructor to use for each Element
    # in the collection, mapping based on the kind value
    class_map = {
        None: Element # Always map the 'default_class'
    }
    
    # Pointers are a 1:1 mapping of 'lookup value' to 'index' within
    # the content list
    pointers = {
        'name': lambda e: e.name,
        'id': lambda e: e.id,
        'path': lambda e: e.path,
        'address': lambda e: e.address
    }

    # Buckets are a 1:* mapping of 'lookup value' to a list of
    # indexes. Bucket functions must return either a hashable
    # object or a list of hashable objects.
    buckets = {
        'pubkey': lambda e: str(e.pubkey)
    }

    # The number of results to render per-page
    page_size = 6
    
    @classmethod
    def sorting_key(cls, data):
        return data.get('created_at', -1)

    # A collection is initialized by passing it a list of json dictionaries
    def __init__(self, elements=[]):
        # Mark when the directory was initialized
        self.ts = Timestamp() 
        self.path = None

        # Make an empty map for each index in the class
        self.maps = {}
        for key in self.pointers:
            self.maps[key] = {}

        for key in self.buckets:
            self.maps[key] = defaultdict(list)

        # We sort the collection by the time each
        # Element was created, most recent last.
        elements.sort(key=self.sorting_key)

        # Populate the content list!
        self.content = []
        for e in elements:
            # First, we construct the element, if necessary
            element = self.hydrate(e)

            self.add(element)

    def __iter__(self):
        return CollectionIterator(self)

    def __len__(self):
        return len(self.content)

    @classmethod
    def load(cls, path_string, **kwargs):
        path = SolarPath.to(path_string)
        recur = kwargs.get('recursive', True)
        data = load_directory(path, recursive=recur)

        if data:
            collection = cls(data)
            collection.path = path
        else:
            collection = cls()

        return collection

    def save(self, **kwargs):
        if self.path:
            default_path = self.path
        else:
            default_path = SolarPath(self.directory, dir=True)

        kwargs['path'] = kwargs.get('path', default_path)
        kwargs['overwrite'] = kwargs.get('overwrite', True)

        # We don't need to update each time when we're 
        # iterating the whole collection
        kwargs['update'] = False

        for element in self.content:
            element.save(**kwargs)

        self.path = default_path

        return self.path

    # all() returns a global variable for the collection, only
    # instantiating once and updating whenever it's called again.
    @classmethod
    def all(cls, **kwargs):
        reload = kwargs.get('reload', False)
        path = kwargs.get('path', cls.directory)

        collection = globals().get(cls.directory)
        if collection is None or reload is True:
            globals()[cls.directory] = cls.load(path)
            collection = globals().get(cls.directory)
            collection.path = SolarPath.to(path or cls.directory, dir=True)

        collection.update()
        return collection

    # Take loaded data and make it into an Element based
    # on the collection's class_map
    def hydrate(self, data):
        if isinstance(data, dict):
            kind = data.get('kind')
            cls = self.class_map.get(kind, self.default_class)
            element = cls(**data)
        else:
            element = data

        return element

    def lookup(self, key, map_name=None):
        index = None
        if isinstance(key, int):
            index = key
        elif map_name:
            index = self.maps[map_name].get(key)
        else:
            # For each index in the collection,
            for map_name in self.pointers:
                # We try to get the key from that map.
                index = self.maps[map_name].get(key)

                # If we find it, return the value!
                if index is not None:
                    break

        return index

    # It may be confusing to have this overlap with
    # The basic "get" function.
    def find(self, key, map_name=None):
        index = self.lookup(key, map_name)

        # Nothing found? return None
        if index is None:
            return None
        
        # If multiple values were found, return a list (filter out null values)
        elif isinstance(index, Iterable):
            return [self.content[i] for i in index if self.content[i] is not None]

        # Else return the referenced value
        else:
            return self.content[index]

    def delete(self, key, map_name=None):
        index = self.lookup(key, map_name)

        # Nothing found? return None
        if index is None:
            return None
        else:
            data = self.content[index]
            self.content[index] = None
            data.unsave()
            return data

    # Add an element to the collection.
    def add(self, element, index=None):

        # Set the element's collection to this object,
        # So it knows where to propagate updates
        element.collection = self

        if index is not None:
            self.content[index] = element

        else:
            self.content.append(element)
            # Get the index of the appended element.
            index = len(self.content) - 1

        # Each index in pointers is a keypair
        # of a "map_name" as the key, and a
        # function for determining the label
        # used to index the content.
        for key, f in self.pointers.items():
            value = f(element)
            if value:
                self.maps[key][value] = index

        for key, f in self.buckets.items():
            values = f(element)
            # Have a a value that isn't in the bucket? add it!

            # Make sure we have a list to iterate through...
            if not isinstance(values, list):
                values = [values]
                
            for value in values:
                if value and index not in self.maps[key][value]:
                    self.maps[key][value].append(index)

    def filter_by(self, index, func):
        # Filtering can be complicated, let's break it down.

        # We choose an index to filter on, and then look through
        # each of those keys. For each key, we apply a function
        # to it, and if that function evaluates to True then it
        # gets added to the 'f' iterator.
        f = filter(func, self.maps[index].keys())
        
        # Once we have the iterator, we use a list comprehension
        # to look up every index we found and return the results.
        if index in self.pointers:
            return [self.find(i, index) for i in f]

    # This function checks the paths associated with the collection
    # to check if anything may need to be added or updated.
    def update(self):
        existing_paths = self.maps['path'].keys()

        # If the collection has been loaded from a path, get
        # an iterator of all files from that path
        if self.path:
            #paths = Path(c.data_folder, self.path).glob(f'**/*{c.file_ext}')
            paths = self.path.children

        # Otherwise, get all the paths that have been mapped
        else:
            paths = existing_paths

        # The number representing the last updated time
        last_updated = self.ts.timestamp()

        # First, go through the existing files and remove anything
        # that is no longer a file.
        deleted = []
        for path in existing_paths:
            if not path.is_file():
                index = self.maps['path'][path]

                # We can't actually remove the item from the content list
                # because it messes with the indexing
                self.content[index] = None
                deleted.append(path)

        added = []
        updated = []
        for path in paths:
            if int(path.stat().st_mtime) >= int(last_updated):
                # load the path to a new element.
                data = load_file(path)
                element = self.hydrate(data)

                # If the path is not indexed, add it.
                index = self.lookup(path, 'path')

                if index is None:
                    self.add(element)
                    added.append(path)

                # Otherwise update it with new values.
                else:
                    self.add(element, index)
                    updated.append(path)

        # finally, update the timestamp!
        self.ts = Timestamp()
        return { 
            'added': added, 
            'updated': updated, 
            'deleted': deleted, 
            'timestamp': self.ts 
        }

    # This function fully remaps the current contents of the collection
    def remap(self):
        self.maps = {}
        for key in self.pointers:
            self.maps[key] = {}

        for key in self.buckets:
            self.maps[key] = defaultdict(list)

        for i, element in enumerate(self.content):
            if element is None:
                continue

            # Then, for each index, we apply the
            # operation to that element and use it
            # as a key for the element's index
            for key, f in self.pointers.items():
                value = f(element)
                if value:
                    self.maps[key][value] = i

            # Likewise, for each bucket we see which
            # entry it belongs to and add the index
            # to that bucket.
            for key, f in self.buckets.items():
                value = f(element)
                
                # If the function returns multiple values,
                # we append each one to the relevant bucket
                if isinstance(value, list):
                    for v in value:
                        self.maps[key][v].append(i)

                # Otherwise we throw it in the bucket!
                elif value:
                    self.maps[key][value].append(i)

    # Sort the collection and remap the indices
    def sort(self):
        self.content.sort(key=lambda e: e.ts)
        self.remap()

    def page(self, index, **kwargs):
        self.update()
        size = kwargs.get('page_size', self.page_size)
        page_start = index * size
        page_end = (index+1) * size

        latest = list(filter(lambda x: x is not None, reversed(self.content)))
        return latest[page_start:page_end]

    def pages(self, size=None):
        if size is None:
            size = self.page_size

        return list(range(1, ceil(len(self.content) / size) + 1))

    # DEPRECATED IN FAVOR OF url()
    # The 'clean path' is the path of the saved element relative to the data folder,
    # excluding the file suffix. This is mainly used for building URLs
    @property
    def clean_path(self):
        if self.path:
            clean = self.path.relative_to(c.data_folder) #/ self.path.stem
            return clean.as_posix()
        else:
            return None

    # The path used to address this element within a URL
    @property
    def url(self):
        base = self.path
        if base:
            return base.url + '/'

    def flatten(self, *args):
        return { 'content': [c.flatten() for c in self.content if c is not None] }

class CollectionIterator:
    def __init__(self, collection):
        self.content = collection.content
        self.counter = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            next_value = None
            # find next non-null value
            while next_value is None:
                count = self.counter
                self.counter += 1
                next_value = self.content[count]
            return next_value
        except IndexError:
            raise StopIteration

