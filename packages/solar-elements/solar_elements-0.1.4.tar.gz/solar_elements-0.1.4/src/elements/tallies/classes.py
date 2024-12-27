from elements.core import Timestamp
from elements.notes import Note, Notes
from elements.core.storage import slugify, SolarPath
import os.path

#                                                
#        |  |  |  |                              
#        |  |  |  |                              
#      ──┼──┼──┼──┼──                            
#        |  |  |  |                              
#        |  |  |  |                              
#                                                
#         Tallies

# A tally is a count that can be attached to another
# element to keep track of a number - this number
# could represent an amount of inventory in stock
# or a wallet balance over time.

# The structure of a Tally note is based on NIP-15's
# standard for a "product".

class Tally(Note):
    directory = 'tallies'
    kind = 30018

    @classmethod
    def on(cls, element, **data):
        if element.name is None:
            raise ValueError('element has no name')

        subject = data.get('subject', 'tally')

        # Try loading an existing tally
        t = Tally.load(os.path.join(cls.directory, element.path.url, subject))
        if t:
            return t

        tags = data.get('tags', [])
        tags.append(['d', subject])
        tags.append(['a', element.address])
        tags.append(['p', element.path.url]) # This should be deprecated in favor of 'a' lookup
        tags.append(['v', data.get('quantity', 0), int(Timestamp())])
        data['tags'] = tags
        data['pubkey'] = element.pubkey

        t = cls.content_dict(**data)
        t._element = element
        return t

    def save(self, **kwargs):
        p = SolarPath.to(self.directory, dir=True) / self.element.path.url
        return Note.save(self, path=p, **kwargs)

    @property
    def element(self):
        try:
            return self._element
        except AttributeError:
            p = self.tags.getfirst('p')
            return Note.load(p)
            

    @element.setter
    def element(self, value):
        self._element = value

    def set(self, count, author=None):
        difference = count - self.count
        self.change(difference, author)

    def change(self, change, author=None):
        v = ['v', change, int(Timestamp())]
        if author:
            v.append(author.pubkey)

        self.tags.add(v)
        self.content['quantity'] = self.count + change

    def from_pubkey(self, pubkey):
        tags = []
        count = 0
        for k, v in self.tags:
            if k == 'v' and len(v) > 2 and v[2] == pubkey:
                tags.append(v)
                count += v[0]

        return { 'count': count, 'tags': tags }

    # Indicates the subject that is being counted
    # (defaults to 'tally')
    @property
    def subject(self):
        return self.content.get('subject', 'tally')

    @property
    def count(self):
        return int(self.content.get('quantity', '0'))

class Tallies(Notes):
    directory = 'tallies'
    default_class = Tally

    class_map = {
        Tally.kind: Tally
    }

    pointers = {
        **Notes.pointers,
        'tally_address': lambda e: e.tags.getfirst('a')
    }

    buckets = {
        **Notes.buckets,
        'subject': lambda e: e.subject
    }

    def sum(self, subject='tally'):
        total = 0
        for tally in self.find(subject, 'subject'):
            total += tally.count
            
        return total



