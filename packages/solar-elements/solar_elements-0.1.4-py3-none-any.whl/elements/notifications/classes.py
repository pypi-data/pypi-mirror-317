from elements.core import Config
from elements.accounts import Accounts
from elements.core.storage import move, SolarPath
from elements.notes import Note, Notes
from pathlib import Path
import os

'''
                       
       ###             
       ###             
       ###             
       ###             
       ###             
       ###             

       /@\             
       \@/             
                       

### Notifications ###

What would a social platform be without
a means to alert you about the latest and
greatest things to happen in the network?

Notifications are a simple Note, containing
the content of the notification and a link
to the relevant post. Each member has a
notifications directory with two folders, 'read'
and 'unread'. Notifications land in the 'unread'
folder and move to 'read' on interaction.

A notification is 'authored' by the member it is
targeted for.

'''

config = Config.load()
scheme = config.SCHEME or 'http://'
host = config.HOST or 'localhost'

accounts = Accounts.all()


class Notification(Note):
    directory = "notifications"

    def __init__(self, **data):
        Note.__init__(self, **data)
        self.read = False
        if self.path:
            folder = os.path.dirname(self.path)
            if not folder.endswith('unread'):
                self.read = True

    @classmethod
    def new(cls, **data):
        data['link'] = scheme + host + data.get('link', '/')
        return cls(**data)

    # Save the notification under the given member name
    # in the appropriate folder
    def save(self, **kwargs):
        kwargs['path'] = Path(self.folder)
        return Note.save(self, **kwargs)

    # Where the notification 'should' be according to its read status.
    @property
    def folder(self):
        if self.read:
            status = "read"
        else:
            status = "unread"

        return SolarPath.to(self.directory, dir=True) / self.author.name / status

    @property
    def notifier(self):
        return self.tags.getfirst('notifier')

    # Move the notification to "read" or "unread" depending on
    # the status passed.
    def mark_as_read(self, status=True):
        if status == self.read:
            return self.path

        if self.path is None:
            raise AttributeError('notification is not saved')

        name = os.path.basename(self.path)
        src = self.folder / name
        self.read = status
        dest = self.folder / name

        if src != dest:
            move(src, dest)

        self.path = dest
        path = self.save()

        return path

    @property
    def account(self):
        author = accounts.find(self.notifier)
        return author
        

    @property
    def link(self):
        return self.tags.getfirst('link') or '/'

# Notifications is loaded on a per-session basis, with each
# member having a Notifications collection
class Notifications(Notes):
    directory = "notifications"
    default_class = Notification

    class_map = {
        Notification.kind: Notification
    }
    
    buckets = {
        'status': lambda e: "unread" if e.read is False else "read"
    }

    @property
    def read(self):
        return list(reversed(self.find('read', map_name="status") or []))

    @property
    def unread(self):
        return list(reversed(self.find('unread', map_name="status") or []))

    # We don't need a global here.
    def all(*args):
        pass

    # Because of how we constantly move notifications
    # between folders, we remap on each update. This
    # may be slightly inefficient, but it doesn't need
    # to be optimized.
    def update(self):
        Notes.update(self)
        Notes.remap(self)

    @classmethod
    def load(cls, member_name):
        path = SolarPath.to(cls.directory) / member_name
        #path = os.path.join(cls.directory, member_name)
        c = super().load(path)
        c.path = path
        return c

    def clear(self):
        for notification in self.unread:
            notification.mark_as_read()
