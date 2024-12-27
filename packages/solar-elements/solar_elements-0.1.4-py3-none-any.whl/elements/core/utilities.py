import json
import urllib

def make_request(url, **kwargs):
    body = kwargs.get('body', {})
    method = kwargs.get('method', 'GET')
    headers = kwargs.get('headers', {})

    data = json.dumps(body).encode()
        
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    return urllib.request.urlopen(req)
