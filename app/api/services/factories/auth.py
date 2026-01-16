from functools import wraps
from flask import request, session, jsonify


def admin_required_with_exceptions(has_exception=False, exception=None):
    """verify if admi role is in session exception in certain cases"""

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if has_exception:
                if request.method == exception:
                    return f(*args, **kwargs)
                
            # if "role" not in session or session["role"] != "admin":
            if "role" not in session:# Accepte n'importe quel rôle connecté pour pouivoir accéder à la ressource

                return jsonify(message="Admin access required"), 403  # Status 403 Forbidden
            return f(*args, **kwargs)

        return decorated_function

    return decorator
