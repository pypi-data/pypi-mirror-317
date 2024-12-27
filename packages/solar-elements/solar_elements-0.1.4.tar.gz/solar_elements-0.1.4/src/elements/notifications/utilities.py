from .classes import Notification
from elements.accounts import Accounts


def notify(member, **kwargs):
    kwargs['author'] = member
    n = Notification.new(**kwargs)
    path = n.save()
    return path

def announce(**kwargs):
    a = Accounts.all()
    role = kwargs.get('role', 'member')

    paths = []
    for member in a.content:
        if role in member.role:
            path = notify(member, **kwargs)
            paths.append(path)

    return paths
