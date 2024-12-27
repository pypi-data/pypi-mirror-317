#from elements.accounts import Member, sessions
#from elements.accounts.nostr import NostrAccount
#from elements.accounts.radicle import RadicleAccount
#from elements.core.nostr import new_event
#
#import textwrap
#
#m = Member.create(master_key=bytes(32), apps=['nostr','radicle'], quick=True)
#n = NostrAccount(m)
#n.login('NPC')
#event = new_event({ 'content': "Hi!" })
#print(n.sign(event))
#print(m.accounts.get('nostr'))
#
#print('\nradicle\n')
#r = RadicleAccount(m)
#r.login('NPC')
#r.save('~/.radicle/keys')
#print(m.accounts.get('radicle'))
#
