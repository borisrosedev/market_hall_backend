from functools import wraps
import uuid
from datetime import datetime as dt
from pathlib import Path
from werkzeug.utils import secure_filename
import os
import re
from flask import request, jsonify


def json_required(f):
    """checks if the request body is valid JSON"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method == "GET":
            return f(*args, **kwargs)
        if not request.is_json:
            return jsonify(message="request body must be in JSON"), 400
        try:
            request.get_json()
        except Exception:
            return jsonify(message="invalid JSON"), 400
        return f(*args, **kwargs)

    return decorated_function
