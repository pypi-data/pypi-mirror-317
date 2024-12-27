import os
import re
import json
import glob
import unicodedata
from hashlib import sha256
from pathlib import Path

from .config import Config

c = Config.load()

'''
Storage is the library responsible for translating data between
the filesystem and the server. It also manages some basic
operations relating to Solar's contextual database system.

'Contextual database system' here refers to the data being
stored in a folder system that holds information based not
only on what the files contain, but also where they are
located in the database. For example: 

* to load all comments, load('comments')
* to load all comments under a 'post' named
'hello-world', load('comments/posts/hello-world') 

'''

# TODO - this needs work. pathlib was updated to be extensible
# in Python3.12, meaning the init override is no longer needed.
# I need a way to selectively enable that code.

# Additionally, the .to() classmethod having a 'dir' flag seems
# to be a bit clunky.

# I think that the best approach is to use SolarPath as an
# interface to the storage module, for reading and writing (TODO)
class SolarPath(Path):
    _flavour = type(Path())._flavour
    def __init__(self, *args, **kwargs):
        Path.__init__(self)
        self.base = Path(c.data_folder)

        # Solar paths always exist in relation to the data folder
        assert self.is_relative_to(self.base)

    @classmethod
    def to(cls, path_string, dir=False):
        p = Path(path_string)

        # Remove 'data/' if passed
        if p.is_relative_to('data/'):
            p = p.relative_to('data/')

        base = Path(c.data_folder)

        if not p.is_relative_to(base):
            p = base / p
        
        if p.is_dir():
            return cls(p)

        # We avoid adding a suffix if dir is True
        if p.suffix == "" and dir is False:
            p = p.with_suffix(c.file_ext)

        return cls(p)
        #if p.is_file():
        #    return cls(p)
        #else:
        #    return None

    # This function will return the contents of the file
    # or folder represented by the path, optionally specifying
    # a subpath of a directory.

    def read(self, subpath=None, **options):
        if subpath:
            path = self / subpath
        else:
            path = self

        if path.is_dir():
            # Note that this function will only load files at
            # the top level of a directory unless recursive=True
            return load_directory(path, **options)
        else:
            return load_file(path)


    @property
    def url(self):
        return self.relative_to(self.base).with_suffix('').as_posix()

    @property
    def dirs(self):
        if not self.is_dir():
            return []

        return [d for d in self.iterdir() if d.is_dir()]

    @property
    def children(self):
        return [d for d in self.rglob(f'**/*{c.file_ext}')]

    #def __repr__(self):
    #    return 'SolarPath representation?'

# This hashes a data structure and returns its sha256sum.
def identify(data):
    data_string = json.dumps(data, separators=(',',':'), ensure_ascii=False)
    return sha256(data_string.encode()).hexdigest()

# This provides a filesafe name from any string passed to it.
def slugify(string):
    slug = unicodedata.normalize('NFKD', string)
    slug = slug.encode('ascii', 'ignore').lower().decode()
    slug = re.sub(r'[^a-z0-9._]+', '-', slug).strip('-')
    slug = re.sub(r'[-]+', '-', slug)
    return slug

## Removes the base from a beginning of a path, and the default file
## extension from the end - if they are present.
#def clean(path):
#    path = re.sub(fr'^{c.base}','', str(path))
#    path = re.sub(fr'{c.file_ext}$','', path)
#    return Path(path)

def save_file(data, **kwargs):
    # Get the path and clean it
    path = kwargs.get('path', '')
    name = kwargs.get('name')
    overwrite = kwargs.get('overwrite')

    if name is None:
        # If we don't have a name, we hash the data
        # And take the first 8 chars - mostly because
        # it looks a bit nicer than 32 chars.
        name = Path(identify(data)[:8])
    else:
        # Otherwise, we make sure it's URL-safe.
        name = Path(slugify(name))

    # Set the file directory and create it if needed
    destination = SolarPath.to(path, dir=True)

    # Make the file folder if it doesn't exist
    destination.mkdir(parents=True, exist_ok=True)

    # Set the write target
    target = destination / name.with_suffix(c.file_ext)
    counter = 0

    # In the case of a conflict, we increment the counter
    # until we've found an open space and write there
    while target.is_file() and overwrite is False:
        counter += 1
        incremented_name = str(name) + f'_{counter}' 
        target = destination / incremented_name.with_suffix(c.file_ext)

    # Write the file!
    with open(target, 'w', encoding="utf8") as f:
        json.dump(data, f, indent=2)

    return SolarPath(target)

def load_file(path, **kwargs):
    if not isinstance(path, SolarPath):
        path = SolarPath.to(path)

    if path.suffix == "":
        path = path.with_suffix(c.file_ext)

    # Loading a single file
    if path.is_file():
        with open(path, encoding="utf8") as file:
            data = json.load(file)

        # TODO - Deprecate
        # This shouldn't happen with new elements
        if isinstance(data, list):
            data[0]['filepath'] = path
        else:
            data['filepath'] = path 

        return data


def load_directory(path, **kwargs):
    # If the path was passed as a string, create a path object
    #if isinstance(path, str):
    #    path = Path(path)

    recursive = kwargs.get('recursive', False)
    sort_by = kwargs.get('sort_by', None)
    #base_path = Path(kwargs.get('data_path', str(c.base)))

    path = SolarPath.to(path)

    ## Add the base path if it's not included
    #if not path.is_relative_to(base_path):
    #    path = Path(base_path) / path

    if not path.is_dir():
        return []
        #err_string = f'Path "{path}" is not a directory'
        #raise ValueError(err_string)

    items = []
    if recursive is True:
        # rglob recurs into directories, glob does not
        directory = path.rglob(f'*{c.file_ext}')
    else:
        directory = path.glob(f'*{c.file_ext}')

    for path in directory:
        file_in_dict = load_file(path) 
        items.append(file_in_dict)

    output = items


    if sort_by is not None:
        try:
            return sorted(output, key=lambda item: item[sort_by])
        except KeyError:
           pass

    return output

def store(file, **kwargs):
    # By default, store the file to uploads unless told otherwise
    path = SolarPath.to(kwargs.get('path', 'uploads'), dir=True)
    path.mkdir(parents=True, exist_ok=True)

    name = slugify(file.name)


    target = path / name
    
    # Here, we seek to the beginning of the file buffer so that we can
    # read the entire thing into a new file
    file.seek(0)
    with open(target, 'wb') as out:
        out.write(file.read())

    file.close()
    return target.relative_to(c.data_folder)

def update():
    # TODO
    pass

def delete(path):
    # Add the base path 
    target = SolarPath.to(path)

    if target.is_dir():
        target.rmdir()
    else:
        target.unlink()

def move(src: SolarPath, dest: SolarPath):
    dest.parent.mkdir(parents=True, exist_ok=True)
    src.rename(dest)

def link(src: SolarPath, dest: SolarPath):
    src.symlink_to(dest)
