import os
import hashlib
import mimetypes
from pathlib import Path
from io import BytesIO
from base64 import b64encode
from urllib.request import urlopen
from PIL import Image, ImageOps

from elements.core import Config
from elements.core.storage import store, link
from elements.notes import Note

'''
Media is an element that deals with file uploads of binary data, usually
in audio, video, and image formats. 

It's a key component for adding visual media to the Solar system,
through avatars and post images.
'''

c = Config.load()

MAX_IMAGE_SIZE = c.MAX_IMAGE_SIZE or 1000000

# Everything in the static/ folder is accessible by querying
# the 'static' path. We symlink data/uploads to static/uploads
# so that everything a member uploads is available via static
# query. 
if c.static_path:
    static = Path(c.host + c.static_path)
else:
    static = Path('static')


class Media(Note):
    directory = "media"
    storage = "uploads"
    kind = 1063

    ## By default, a Media object is instantiated by passing a file-like
    ## object as the first argument, along with associated metadata
    @classmethod
    def new(cls, file, metadata = {}):
        file.seek(0)
        fbytes = file.read()
        size = len(fbytes)
        sha256 = hashlib.sha256(fbytes).hexdigest()

        # Added an override for file.name, because
        # It doesn't work with Bottle uploads
        name = metadata.get('name', file.name)

        # The values we add here 
        data = {
            **metadata,
            'm': mimetypes.guess_type(name, strict=False)[0],
            'x': sha256,
            'size': size
        }

        n = cls(**data)
        n.file = file
        return n

    @classmethod
    def from_link(cls, link, metadata={}):
        file = urlopen(link)
        return cls.new(file, metadata={})

    @classmethod
    def from_local(cls, filepath, metadata={}):
        file = open(filepath, 'rb')
        return cls.new(file, metadata={})

    # Saving the media object starts by saving the file object into
    # a publically accessible location if not available, followed by 
    # saving the Media element itself, in a separate location.
    def save(self, **kwargs):

        # The storage directory is the default location
        storage = kwargs.get('storage', self.storage)
        note_directory = kwargs.get('directory', self.directory)

        # If there's no URL, we need to store the media.
        url = self.tags.get('url')
        if url is None:
            author = self.author.name

            # This path is the directory where we will save the data provided.
            path = os.path.join(self.storage, author)

            self.store(path)

            # This value is the directory where we will store the saved element.
            kwargs['path'] = kwargs.get(path, os.path.join(self.directory, author))

            # Name is the actual name of the saved element.
            kwargs['name'] = kwargs.get('name', os.path.splitext(self.file.name)[0])

        return Note.save(self, **kwargs)

    # Storing the media object saves the media onto the local filesystem 
    # and references the file location in the metadata
    def store(self, path = None):
        # We need to make sure that the uploads directory is linked
        # in the static directory.
        path = Path('static/uploads')
        if not path.is_symlink():
            path.symlink_to('../data/uploads')

        target_directory = Path('uploads') / self.author.name 

        path = store(self.file, path=target_directory)
        url = static / path
        self.tags.add(['url', c.scheme + str(url)])

        # We save the file in the data directory,
        # returning the relative location from there
        return path

    @property
    def static_url(self):
        return self.tags.getfirst('url')

    # Return the thumbnail if it exists, or the full img

    @property
    def preview_url(self):
        return self.tags.getfirst('thumb') or self.tags.getfirst('url')

    # Shorthand for exporting the media as a standard tag
    @property
    def inline(self):
        inline_metadata = ['imeta']
        for tag in self.tags.flatten():
            # Here, we use a 'list comprehension' to cast everything
            # as a string before joining into a space-separated list
            inline_metadata.append(' '.join(str(t) for t in tag))

        return inline_metadata

    @property
    def name(self):
        if self.path:
            return self.path.stem
        else:
            return self.tags.getfirst('d')



# Pillow is a massive library (11MB!) to integrate for a small task.
# I have considered using ImageMagick bindings but the implementation
# I tried (Wand) was clunkier than I would like. 

class Picture(Media):
    @classmethod
    def new(cls, file, **metadata):
        # We set the max dimensions of a new picture to 800x600 unless
        # specified otherwise
        dimensions = metadata.pop('dimensions', (800,600))
        image_format = metadata.pop('format', 'JPEG')
        
        # Read file into fbytes to be hashed; reset it
        fbytes = file.read()
        file.seek(0)

        # We are resizing the file, so we save the original hash
        # and pass it as a piece of metadata
        sha256 = hashlib.sha256(fbytes).hexdigest()
        metadata['ox'] = sha256

        with Image.open(file) as img:
            file_buffer = BytesIO()
            write_dimensions = (min(dimensions[0], img.size[0]), min(dimensions[1], img.size[1]))

            # This is needed to flatten png files to JPG
            img = img.convert('RGB')
            img = ImageOps.exif_transpose(img) # Rotate according to exif data
            img = ImageOps.contain(img, write_dimensions, Image.LANCZOS)
            img.save(file_buffer, format=image_format)
        
            # We look for a value 'name' in the metadata, if it doesn't 
            # exist then we use the existing name for the file.
            basename = metadata.pop('name', None) or os.path.basename(file.name)

            # We only support these two formats right now. Might be
            # worthwhile to add GIFs
            if image_format == "PNG":
                format_suffix = '.png'
            else:
                format_suffix = '.jpg'

            img_name = os.path.splitext(basename)[0] + format_suffix
            file_buffer.name = img_name

            # Once we've copied the imgbytes to a new buffer,
            # we close the original file to prevent memory leaks.
            file.close()

        metadata['dim'] = f'{write_dimensions[0]}x{write_dimensions[1]}'

        return super().new(file_buffer, metadata)

    def thumbnail(self, **kwargs):
        dimensions = kwargs.get('dimensions', (80,60))
        path = kwargs.get('path', None)
        with Image.open(self.file) as img:
            file_buffer = BytesIO()
            img = ImageOps.fit(img, dimensions, Image.LANCZOS)
            img.save(file_buffer, format="PNG")
            file_buffer.name = self.file.name

            # We may not need this.
            b64_image = b64encode(file_buffer.getvalue()).decode()
            thumbnail = f'data:image/png;charset=utf-8;base64,{b64_image}'

            # This may be better as uploads/<author>/thumbnails?
            target_directory = Path('uploads', self.author.name, 'thumbnails')
            path = store(file_buffer, path=target_directory)
            self.tags.add(['thumb', c.scheme + str(static / path)])

            return thumbnail
