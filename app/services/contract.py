from functools import wraps
import uuid
from datetime import datetime as dt
from pathlib import Path 
from werkzeug.utils import secure_filename
import os
import re
from flask import request, jsonify

EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"


# Decorators 
def multipart_form_required(f):
    pass



def file_required(f):
    pass

def image_required(f):
    pass


def json_required(f):
    """ checks if the request body is valid JSON """
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


def unique_filename_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method == "GET":
            return f(*args, **kwargs)
        file = request.files['file']
        filename = secure_filename(file.filename)
        name, ext = os.path.splitext(filename)
        unique_id = uuid.uuid4().hex
        timestamp = dt.now().strftime('%Y%m%d-%H%M%S')
        unique_name = f"{name}-{timestamp}-{unique_id}{ext}"
        return f(*args, **kwargs, unique_name=unique_name)
    return decorated_function


# Decorators's Fabrics




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
            print("✅")
            print(data)
            print("---")
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
            print("here❤️")
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def json_required_with_keys(*required_keys):
    """ verify if required keys are in the JSON """
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


def json_required_with_validation(*required_keys, email_key='email', password_key='password', min_password_length=8):
    """  verify if required keys are in the JSON and apply by validation rules """
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
                return jsonify(message=f"Password must have a least {min_password_length} characters"), 400

            return f(*args, **kwargs)
        return decorated_function
    return decorator
