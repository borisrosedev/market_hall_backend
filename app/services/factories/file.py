
from functools import wraps
import uuid
from datetime import datetime as dt
from pathlib import Path 
from werkzeug.utils import secure_filename
import os
import re
from flask import request, jsonify

# Decorators's Factory


def file_required_with_specific_extensions(*required_keys):
    pass 
 
def multipart_form_data_with_specific_extension_file_and_keys(files_extensions: list[str],required_keys: list[str]):
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
                return jsonify(message=f"Keys missing in multipart-form-data : {', '.join(missing_keys)}"), 400
            if 'file' not in request.files:
                return jsonify(message="file missing"), 400
            file = request.files['file']
            if file.filename == '':
                return jsonify(message="no selected file"), 400
            ext = file.filename.rsplit('.', 1)[-1].lower()
            if ext not in files_extensions:
                return jsonify(message="file extension not allowed"), 400
            return f(*args, **kwargs)
        return decorated_function
    return decorator
