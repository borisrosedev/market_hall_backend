import os
import re
from functools import wraps
import uuid
from datetime import datetime as dt
from pathlib import Path
from werkzeug.utils import secure_filename
from flask import request, jsonify


# Decorators


def multipart_form_data_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        ctype = request.headers.get("Content-Type", "")
        if "multipart/form-data" not in ctype:
            return jsonify(message="Content-Type must be multipart/form-data"), 400
        return f(*args, **kwargs)

    return decorated_function


def file_required(f):
    """file is required"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.is_json:
            return f(*args, **kwargs)
        if request.method in ("POST", "PUT", "PATCH"):
            if "file" not in request.files:
                return jsonify(message="file missing"), 400
            filename = secure_filename(request.files["file"].filename)
            name, ext = os.path.splitext(filename)
            if name == "" or ext == "":
                return jsonify(message="part file missing"), 400
        return f(*args, **kwargs)

    return decorated_function


def image_required(f):
    """image type file is required"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.is_json:
            return f(*args, **kwargs)
        if request.method in ("GET", "DELETE"):
            return f(*args, **kwargs)
        file = request.files["file"]
        filename = secure_filename(file.filename)
        _, ext = os.path.splitext(filename)
        allowed_extensions = {"png", "jpg", "jpeg", "gif", "webp"}
        if ext.replace(".", "") not in allowed_extensions:
            return jsonify(message="invalid type file "), 400
        return f(*args, **kwargs)

    return decorated_function


def unique_filename_required(f):
    """makes sure the file will have a unique name afterwards"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method in ("GET", "DELETE"):
            return f(*args, **kwargs)
        if request.is_json:
            return f(*args, **kwargs)
        file = request.files["file"]
        if not file:
            return f(*args, **kwargs)
        filename = secure_filename(file.filename)
        name, ext = os.path.splitext(filename)
        unique_id = uuid.uuid4().hex
        timestamp = dt.now().strftime("%Y%m%d-%H%M%S")
        unique_name = f"{name}-{timestamp}-{unique_id}{ext}"
        return f(*args, **kwargs, unique_name=unique_name)

    return decorated_function
