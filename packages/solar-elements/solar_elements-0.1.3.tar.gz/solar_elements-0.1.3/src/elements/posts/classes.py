import mimetypes
from math import ceil
from markdown import markdown

from elements.core import Timestamp
from elements.core.storage import slugify
from elements.accounts import Account, Accounts
from elements.media import Picture, Media
from elements.notes import Note, Notes

'''

    ################
    #              #
    #    Posts     #
    #              #
    ################
           |
           |
          \|/

Posts are the bread-and-butter of the Solar
system. Most of the time, someone making a
contribution to the system will do so by
making a Post.

A Post contains parseable markdown in the
content body. It may also contain convenience
functions for linking media components
as tags of ['media', 'media/npc/test'] which
will be hydrated on load and exported in
accordance with NIP-92 (media attachments).

'''

accounts = Accounts.all()

class Post(Note):
    directory = 'posts'
    kind = 30023

    def __init__(self, **data):
        Note.__init__(self, **data)
        if self.tags.get('published_at') is None:
            self.tags.add(['published_at', int(self.created_at)])

        self.media = {}
        self.load_media()

    @property
    def name(self):
        title = self.tags.getfirst('title')
        if title:
            return slugify(title)
        else:
            return super().name

    # Attach a file to the post as a media component
    def attach(self, upload, **kwargs):
        # When using local files, the name is file.name.
        # Here, because we're using Bottle FileUploads it
        # is file.filename.
        mimetype = mimetypes.guess_type(upload.filename, strict=False)[0]


        if mimetype.startswith('image'):
            m = Picture.new(upload.file, **{ 'name': upload.filename, 'author': self.author })
            
            # If 'thumbnail' is passed, use the values to generate
            # a thumbnail of the attached image before saving.
            thumbnail = kwargs.get('thumbnail')
            if thumbnail:
                m.thumbnail(dimensions=thumbnail)
        else:
            m = Media.new(file, { 'name': upload.filename, 'author': str(self.author) })

        path = m.save()
        self.tags.add(['media', str(path)])
        self.tags.add(m.inline)
        self.load_media(path)
    
        return m

    # Load Media inflates the Media data for 
    # each path in the tags, or for a specific
    # Media path.
    def load_media(self, path=None):
        if path:
            m = Media.load(path)
            self.media[m.name] = m
            return m

        tags = self.tags.getall('media')
            
        for t, *_ in tags:
            m = Media.load(t)
            self.media[m.name] = m

        return self.media

    @property
    def meta(self):
        return self.tags.metadata

    @property
    def published_at(self):
        return Timestamp(self.tags.getfirst('published_at'))

    # This is the property we use to parse
    # the post's markdown content into HTML
    #
    # It could stand to include a HTML sanitizing
    # library like 'bleach' to avoid XSS. I think
    # that this will work well enough though.
    @property
    def html(self):
        sanitized = self.content.replace('<', '&lt;').replace('>', '&gt;')
        return markdown(sanitized)

    def truncated_html(self, number_of_chars=200):
        sanitized = self.content[:number_of_chars].replace('<', '&lt;').replace('>', '&gt;')
        return markdown(sanitized)

    # TODO: I should probably update this to be
    # a bit less janky... later tho
    @property
    def first_media(self):
        if len(self.media) > 0:
            return next(iter(self.media.values()))

        return None

class Posts(Notes):
    default_class = Post
    directory = "posts"
    pointers = {
        'name': lambda e: e.name,
        'path': lambda e: e.path,
        'route': lambda e: e.clean_path,
    }

    buckets = {
        'author': lambda e: e.author.name
    }

    class_map = {
        Post.kind: Post
    }

    @classmethod
    def sorting_key(cls, data):
        for t in data.get('tags'):
            if t[0] == "published_at":
                return t[1]

        return data.get('created_at')

    def by_author(self, author_name):
        return self.find(author_name, map_name="author")
