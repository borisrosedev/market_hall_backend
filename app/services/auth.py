from functools import wraps
from flask import session, jsonify, request


def admin_required_with_exceptions(has_exception = False, exception=None):
    """ verify if admi role is in session exception in certain cases"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if has_exception:
                if request.method == exception:
                    return f(*args, **kwargs)
            if 'role' not in session or session['role'] != 'admin':
                return jsonify(message="Admin access required"), 403  # Status 403 Forbidden 
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    """ verify if role admin is in session """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'role' not in session or session['role'] != 'admin':
            return jsonify(message="Admin access required"), 403  # Status 403 Forbidden 
        return f(*args, **kwargs)
    return decorated_function


def session_required(f):
    """ verify if email is in session """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session:
            return jsonify(message="Authentication required"), 401 # Status 401 Unauthorized
        return f(*args, **kwargs)
    return decorated_function