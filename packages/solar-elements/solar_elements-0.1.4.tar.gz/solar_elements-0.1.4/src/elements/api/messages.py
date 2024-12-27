import os
import json
from elements.core import request, response
from elements.accounts import Account
from elements.accounts.utilities import lookup
from elements.messages import Message, Conversation
from elements.api.utilities import verify_request

'''

Messaging API allows for server-to-server messaging.
It exposes an endpoint for sharing conversation
objects.

'''
def conversation(path="conversations/a1b2c3d4"):
    # TODO: Verify that this author has permission
    # to send data to the server.
    author = verify_request()
    conversation = Conversation.load(path)


    if request.method == "POST":
        body = request.body.read()
        data = json.loads(body.decode())
        if conversation:
            conversation.merge(data)
            path = conversation.save()
            response.status = 202
        else:
            conversation = Conversation(data)
            names = conversation.content.get('people').keys()
            for name in names:
                n = lookup(name, request=False)
                if isinstance(n, Account):
                    # If they're a member, save this to their
                    # list of conversations
                    n.conversation_list.add(['conversation', conversation.name, *names])
                    n.save()
                
            path = conversation.save()
            response.status = 200

    return json.dumps(conversation.flatten())
