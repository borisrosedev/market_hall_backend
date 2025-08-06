from functools import wraps
from flask import session, jsonify

def session_required(f):
    """ verify if email is in session """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session:
            return jsonify(message="Authentication required"), 401
        return f(*args, **kwargs)
    return decorated_function