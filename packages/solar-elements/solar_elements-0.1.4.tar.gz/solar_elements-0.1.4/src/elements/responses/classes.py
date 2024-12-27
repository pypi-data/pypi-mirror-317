import os 

from elements.core.storage import SolarPath
from elements.accounts import Accounts
from elements.notes import Note, Notes


'''
                              
  ###################         
 #                   #        
 #            1      #  
 #           11      #  
 #    +       1      #  
 #  +++++     1      #  
 #    +       1      #  
 #            1      #  
 #          11111    #  
 #                   #        
  ###################         
                              
Responses are another huge part of social platforms.
A response can be any sort of shorthand acknowledgement
of a post, including 'likes' or 'up/downvotes'.

'target' is the piece of content that is being responded
to.

'''          

class Response(Note):
    directory = "responses"
    kind = 7
    target_class = Note

    @property
    def target(self):
        target_path = self.tags.getfirst('target')
        if target_path: 
            return self.target_class.load(target_path)

        return None

    @classmethod
    def new(cls, content="+", **kwargs):
        target = kwargs.get('target')

        if target is None:
            raise AttributeError('response needs a "target" element')
        
        kwargs['target'] = target.path.url
        kwargs['content'] = content

        return cls(**kwargs)

    def save(self, **kwargs):
            # By default, a response saves to a path based on the response target,
            # with a name of the response author, one response on a post per person!
            path = os.path.join(self.directory, self.target.path.url)
            kwargs['path'] = kwargs.get('path', path)
            kwargs['name'] = kwargs.get('name', self.author.name)
            return Note.save(self, **kwargs)

class Responses(Notes):
    default_class = Response 
    directory = "responses"

    class_map = {
        **Notes.class_map,
        default_class.kind: default_class
    }

    buckets = {
        'author': lambda e: e.author.name,

        # A bucket for all the responses to a given element,
        # indexed by its data path
        'target': lambda e: e.tags.getfirst('target')
    }

    @classmethod
    def on(cls, element, **data):
        if element.name is None:
            raise ValueError('element has no name')

        if element.path is None:
            raise ValueError('element has no url')

        path = SolarPath.to(cls.directory, dir=True) / element.url
        return cls.load(path)
