import os

from elements.core import Element, Collection, Timestamp, identify
from elements.core.encryption import encrypt, decrypt, decrypt_or, shared_key
from elements.accounts.utilities import lookup

from secp256k1 import PrivateKey

'''
                                
                                
             @@@@@@@@@@@@@                 
            @             @                
           @               @               
           @   >messages   @               
           @               @               
            @             @                
             @@@@@@@@@@@@@                 
                        \|

What would socials be without mogging your rizz
to slide into someone's DMs and ask them to 
spill the tea on their latest subtweet?
(one day, this paragraph will be unintelligible)

Messages implements basic text communication
between two or more members in the system. Conversations
are encrypted with a shared key saved in the tags
of the conversation object.

Unlike some other Elements, Conversations are not a global
object. The conversation set is loaded and decrypted on
session initialization, then attached to the session object

'''

class Message(Element):
    def __init__(self, data):
        Element.__init__(self, data)
        self.message = None

    @classmethod
    def new(cls, key, **kwargs):
        content = kwargs.get('content')
        if content:
            encrypted = encrypt(content, key)
            kwargs['content'] = encrypted.decode()

        m = Message(kwargs)
        m.message = content
        return m

    def decrypt(self, key):
        self.message = decrypt(self.content, key)
        return self.message

    # Return the message along with the member's profile.
    # If a 'new_since' value is passed, we mark some messages
    # as "new".
    def display(self, profiles, new_since=None):
        profile = profiles.get(self.author)
        profile.content['name'] = profile.display_name or self.author
        
        if new_since and new_since < int(self.ts):
            new = True
        else:
            new = False

        return { 
            'message': self.message,
            'profile': profile, 
            'sent': self.ts,
            'new': new
        }


class Conversation(Collection):
    directory = 'conversations'
    default_class = Message
    class_map = {}

    def __init__(self, data=[{}]):
        Collection.__init__(self, data)


        self.private_key = None
    
    # Conversations are indexed by their public key
    @property
    def name(self):
        return self.content.get('public_key')

    @property
    def profiles(self):
        values = {}
        for name in self.content.get('people'):
            member = lookup(name, request=False)
            if member is None or member.pubkey is None:
                continue

            values[name] = member.profile

        return values


    # This is a convenience function for returning messages in a format
    # that can be easily rendered on a webpage
    def messages(self, since=0, last_seen=None):
        if self.private_key is None:
            return []
        elif last_seen:
            return [msg.display(self.profiles, last_seen) for msg in self.components if int(msg.ts) > since]
        else:
            return [msg.display(self.profiles) for msg in self.components if int(msg.ts) > since]
    
    @classmethod
    def new(cls, *args):
        # Each argument is a member name to be looked up and
        # added to the conversation

        key = PrivateKey()

        # We use this private key to encrypt the conversation, and
        # encrypt it with a shared_key for each member.
        private_key = key.private_key.hex()

        # The public key is saved in the content in order to generate the
        # shared key.
        public_key = key.pubkey.serialize().hex()

        people = {}
        now = int(Timestamp())

        for name in args:
            account = lookup(name)
            if account is None or account.pubkey is None:
                continue

            account_key,  _ = shared_key(private_key, account.pubkey)
            conversation_key = encrypt(private_key, account_key)

            remote = None

            #if isinstance(account, NPC):
            #    raise AttributeError('fix this!')
            #    name, host = account.name.split('@')
            #    remote = host
            #else:

            account.conversation_list.add(['conversation', public_key, *args])
            account.save()

            people[account.name] = { 
                'last_seen': now, 
                'conversation_key': conversation_key.decode(),
                'remote': remote
            }


        c = cls([{ 'content': { 'people': people, 'public_key': public_key }}])
        c.private_key = bytes.fromhex(private_key)
        c.save()

        return c

    def auth(self, name, private_key):
        # We get information for the given member
        person = self.content['people'].get(name)

        # We create a shared key with the group
        key1, key2 = shared_key(private_key, self.content['public_key'])

        # We use that shared key to decrypt the conversation key
        conversation_key = decrypt_or(person.get('conversation_key'), key1, key2)
        self.private_key = bytes.fromhex(conversation_key)
        
        # We decrypt all the messages in the conversation!
        for message in self.components:
            message.decrypt(self.private_key)

        return conversation_key
        
    # Creates a new message and adds it to the compound
    def message(self, **kwargs):
        content = kwargs.get('content')
        m = Message.new(self.private_key, **kwargs)
        m.compound = self
        self.components.append(m)
        m.save()
        return m

    # Merges the contents of two conversations
    def merge(self, updates):
        index, *messages = updates
        people = index['content']['people']
        for person in people:
            remote_time = people[person].get('last_seen')
            local_time = self.content['people'][person].get('last_seen')
            self.content['people'][person]['last_seen'] = max(remote_time, local_time)

        existing_ids = [m.id for m in self.components]
        new_ids = []

        # n^2 complexity
        for message in messages:
            message_id = identify(message) 
            if message_id not in existing_ids:
                new_message = Message(message)
                self.components.append(new_message)
                new_ids.append(new_message.id)

        return {"added": new_ids}

class Conversations(Collection):
    #pointers = {
    #    'name': lambda e: e.name,
    #    'path': lambda e: e.path
    #}

    @classmethod
    def sorting_key(cls, data):
        return data.ts

    # load the conversations of a member by their
    # session object
    @classmethod
    def load(cls, session):
        name = str(session.author)
        member = lookup(name)
        k = session.content.get('solar')
        member.conversation_list.auth(k)
        conversation_keys = member.conversation_list.items.getall('conversation')

        conversations = []
        for key, *_ in conversation_keys:
            c = Conversation.load(os.path.join('conversations', key))
            c.auth(name, k)
            conversations.append(c)

        c = cls(conversations)
        c.conversation_list = member.conversation_list.items
        c.session = session
        return c

    #TODO: This is untested
    def update(self):
        session = self.session

        name = str(session.author)
        member = lookup(name)
        k = session.content.get('solar')
        member.conversation_list.auth(k)
        conversation_keys = member.conversation_list.items.getall('conversation')

        conversations = []
        for key, *_ in conversation_keys:
            c = Conversation.load(os.path.join('conversations', key))
            c.auth(name, k)
            conversations.append(c)

        self.contents = conversations
        self.remap()

    # We can't lookup the names in the conversations by default, so we use
    # The member's conversation lists to get them by name and # of people
    def lookup_names(self, *names, size=None):
        keys = []
        # For each conversation in the members list,
        for _, entry in self.conversation_list:
            key, *c_names = entry
        
            # If we're looking for a specific size of conversation,
            # skip any that don't match that size
            if size and size != len(c_names):
                continue

            match = True
            for name in names:
                if name not in c_names:
                    match = False

            # We append if the name is in there.
            if match == True:
                keys.append({ 'key': key, 'names': c_names })

        # If we only found one key, return it directly
        if len(keys) == 1:
            return keys[0].get('key')
        elif len(keys) == 0:
            return None
        else:
            return keys
        
