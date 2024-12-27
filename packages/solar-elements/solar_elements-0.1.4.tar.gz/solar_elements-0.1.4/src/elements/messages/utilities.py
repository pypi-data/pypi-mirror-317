import json
from elements.messages import Conversation, Conversations
from elements.accounts.utilities import lookup
from elements.api.utilities import auth_request

# This utility creates a new 1-to-1 conversation,
# either for members on the same server or on
# different servers.
def send_direct_message(session, address, message_content, force_remote=None):
    message_author = session.member.name
    chats = Conversations.load(session)
    chat_key = chats.lookup_names(address, size=2)
    if chat_key is None:
        lookup(address, member=session.member)
        chat = Conversation.new(message_author, address)
    elif isinstance(chat_key, list):
        raise ValueError("Ambiguous chat lookup - can't decide where to send the message")
    else:
        chat = chats.find(chat_key)

    chat.message(content=message_content, author=message_author)
    other_person = chat.content['people'][address]
    
    remote = other_person.get('remote')

    # This is only used for testing the API in a local environment.
    if force_remote:
        remote = force_remote

    if remote:
        # If we're chatting to someone remotely, we send the conversation to their server.
        response = auth_request(f'http://{remote}/conversations/{chat.name}/conversation', 
                    body=chat.flatten(), 
                    method="POST",
                    headers={'Content-Type': 'application/json'},
                    session=session,
                    authorization="Nostr")

        # Response 200? All good, nothing new.
        if response.status == 200:
            pass
    
        # Response 202? We've got updates.
        elif response.status == 202:
            updates = json.load(response)
            chat.merge(updates)

    chat.save()
    return chat

# Maybe a bit later...
def start_group_conversation(session, *addresses):
   pass
        #for person in people:
        #    remote = people[person].get('remote')
        #    if remote:
        #        response = auth_request(f'http://{remote}/conversations/{existing_chat.name}/message', 
        #                    body=message.flatten(), 
        #                    method="POST",
        #                    session=session)

        #        if response.status == 200:
        #            continue
        #        elif response.status == 202:
        #            updates = json.load(r)
        #            divergence.append(updates)

        #    for updates in divergence:
        #           existing_chat.merge(updates)
    

