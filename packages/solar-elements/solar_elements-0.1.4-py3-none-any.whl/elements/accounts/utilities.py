import json
from elements.core import Collection, Config, make_request

from elements.accounts import Account, Accounts, Placeholder

def lookup(value):
    accounts = Accounts.all()
    account = accounts.find(value)
    if account:
        return account
    else:

        # Eventually, this will be able to look up from
        # a remote source designated in the note.
        return Placeholder()

#from elements.accounts import Members, Guest, Guests
#
#c = Config.load()
#members = Members.all()
#guests = Guests.all()
#
#def lookup(value, member="npc", request=True):
#    # If the value has an @, we lookup from there.
#    if '@' in value:
#        value, host = value.split('@')
#    else:
#        host = c.host
#
#    if host in ["localhost", c.host]:
#        members.update()
#        member = members.find(value)
#        return member
#    else:
#        name = f'{value}@{host}'
#        guest = guests.find(name)
#
#        # If we didn't find the guest among our existing guests,
#        # we check to see if we're allowed to request the data
#        # from another server and then save that data locally
#        # if we find it.
#        if guest is None and request is True:
#            res = make_request(f'http://{host}/.well-known/nostr.json')
#            data = json.load(res)
#            pubkey = data['names'].get(value)
#            if pubkey is None:
#                return None
#
#            # This 'guest account' is authored by the member who invited
#            # them to the system.
#            content = { 'name': name, 'pubkey': pubkey, 'author': member }
#            
#            # Profiles maps member pubkeys to kind 0 metadata
#            profiles = data.get('profiles')
#            
#            if profiles:
#                content.update(profiles.get(pubkey))
#
#            g = Guest(content)
#            guests.add(g)
#            g.save()
#
#            return g
#
#        else:
#            return guest
            
                

        
