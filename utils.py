from models import *


def key_is_valid(req):
    if 'key' in req.headers and Clients.exists(lambda c: c.api_key.key == req.headers['key']):
        return True
    return False
