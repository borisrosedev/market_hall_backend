from functools import wraps
import uuid
from datetime import datetime as dt
from pathlib import Path
from werkzeug.utils import secure_filename
import os
import re
from flask import request, jsonify

# Decorators's Factory


def multipart_form_data_with_specific_extension_file(file_key="file", allowed_exts=None):
    if allowed_exts is not None:
        allowed_exts = {ext.lower().lstrip(".") for ext in allowed_exts}

    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            ctype = request.headers.get("Content-Type", "")
            if "multipart/form-data" not in ctype:
                return jsonify(message="Content-Type must be multipart/form-data"), 400

            if file_key not in request.files:
                return jsonify(message=f'part "{file_key}" missing'), 400

            file = request.files[file_key]

            filename = secure_filename(file.filename or "")
            if not filename:
                return jsonify(message="empty filename"), 400

            name, ext = os.path.splitext(filename)
            if not name or not ext:
                return jsonify(message="filename must include an extension"), 400

            ext_clean = ext.lower().lstrip(".")
            if allowed_exts and ext_clean not in allowed_exts:
                return jsonify(message=f'extension ".{ext_clean}" not allowed'), 400

            return f(*args, **kwargs)

        return wrapped

    return decorator


def multipart_form_data_with_specific_extension_file_and_keys(
    files_extensions: list[str], required_keys: list[str]
):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if request.method == "GET":
                return f(*args, **kwargs)
            data = request.form
            if not data:
                return jsonify(message="multipart form data required"), 400
            missing_keys = [key for key in required_keys if key not in data.keys()]
            if missing_keys:
                return jsonify(
                    message=f"Keys missing in multipart-form-data : {', '.join(missing_keys)}"
                ), 400
            if "file" not in request.files:
                return jsonify(message="file missing"), 400
            file = request.files["file"]
            if file.filename == "":
                return jsonify(message="no selected file"), 400
            ext = file.filename.rsplit(".", 1)[-1].lower()
            if ext not in files_extensions:
                return jsonify(message="file extension not allowed"), 400
            return f(*args, **kwargs)

        return decorated_function

    return decorator
