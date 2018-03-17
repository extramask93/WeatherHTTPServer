from functools import wraps
from flask import session

def LoginRequired(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if('logged_in' in session):
            return f(*args, **kwargs)
        else:
            return {'message': 'Please log in'},511
    return wrap