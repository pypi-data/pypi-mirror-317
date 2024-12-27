from elements.core import Element, Collection, Config
from elements.core.storage import SolarPath
import elements

c = Config.load()


#     __________            
#    |=========|\           
#    |=========| \          
#    |=========|__\         
#    |============|         
#    |= Database =|         
#    |============|         
#    |============|         
#    |____________|         

'''
A 'database' is a collection of information
that is often changing and needs to be accessed
and updated regularly.

The default database in Solar is FileDatabase,
which loads data from plaintext files in Solar's
assigned 'data' folder.

It acts as an abstraction layer to direct queries
to the correct "Collection" object and returns
the instantied object representing that kind of
data.
'''

class FileDatabase:
    def __init__(self, data_folder):
        self.data_folder = data_folder
        self.collections = {}

        # This fancy bit of code gets every attribute from
        # the imported 'elements' and filters through for
        # ones that inherit Collection. Then, it saves the
        # global collection to the dictionary so that it
        # can be looked up based on the file's path.
        for name in dir(elements):
            element = getattr(elements, name)
            try:
                if issubclass(element, Collection):
                    collection = element.all()
                    label = element.directory
                    if collection is not None:
                        self.collections[label] = element.all()
            except TypeError:
                # Not a class
                pass

    def load(self, path):
        directory = path.split('/')[0]
        collection = self.collections.get(directory)

        if collection:
            location = SolarPath.to(path)

            return collection.find(location)

            # TODO: revisit loading a directory
            # This seems more complex than necessary
            #if str(location).endswith(collection.directory):
            #    return collection.load(path)
            #else:
            #    return collection.find(location)
        else:
            return Element.load(path)
            return None

    # This allows collections to be accessed from the database object
    # (e.g. db.notes)
    def __getattr__(self, attr):
        return self.collections.get(attr)

class FutrDatabase:
# Eventually, I will wire Futr into the Solar System
# so that data can be queried directly from everything
# saved via Nostr. Not today, though.
    pass
