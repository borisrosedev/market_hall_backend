from functools import wraps
import uuid
from datetime import datetime as dt
from pathlib import Path
from werkzeug.utils import secure_filename
import os
import re
from flask import request, jsonify

EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"


def json_required_with_keys(*required_keys):
    """verify if required keys are in the JSON"""

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if request.method == "GET":
                return f(*args, **kwargs)
            if not request.is_json:
                return jsonify(message="request body must be in JSON"), 400
            try:
                data = request.get_json()
            except Exception:
                return jsonify(message="invalid JSON"), 400

            missing_keys = [key for key in required_keys if key not in data]
            if missing_keys:
                return jsonify(message=f"Keys missing in JSON : {', '.join(missing_keys)}"), 400

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def json_required_with_validation(
    *required_keys, email_key="email", password_key="password", min_password_length=8
):
    """verify if required keys are in the JSON and apply by validation rules"""

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if request.method == "GET":
                return f(*args, **kwargs)
            if not request.is_json:
                return jsonify(message="request body must be in JSON"), 400
            try:
                data = request.get_json()
            except Exception:
                return jsonify(message="invalid JSON"), 400

            missing_keys = [key for key in required_keys if key not in data]
            if missing_keys:
                return jsonify(message=f"Keys missing in JSON : {', '.join(missing_keys)}"), 400

            email = data.get(email_key)
            if email is not None and not re.match(EMAIL_REGEX, email):
                return jsonify(message="Invalid email"), 400

            password = data.get(password_key)
            if password is not None and len(password) < min_password_length:
                return jsonify(
                    message=f"Password must have a least {min_password_length} characters"
                ), 400

            return f(*args, **kwargs)

        return decorated_function

    return decorator
