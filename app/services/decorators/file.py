from functools import wraps
import uuid
from datetime import datetime as dt
from pathlib import Path 
from werkzeug.utils import secure_filename
import os
import re
from flask import request, jsonify

from app.services.decorators.info import test_info_request

# Decorators 
def multipart_form_required(f):
    """ multipart required """ 
    @wraps(f)
    def decorated_function(*args, **kwargs):
        #test_info_request(request)
         
        file = request.files['file']
        filename = secure_filename(file.filename)
        name, ext = os.path.splitext(filename)
        if name == '' or ext == '':
            return jsonify(message="part file missing"), 400
        return f(*args, **kwargs )
    return decorated_function


def file_required(f): 
    """ image file is required """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method == 'POST':
            if 'file' not in request.files:
                return jsonify(message="file missing"), 400
        return f(*args, **kwargs)
    
    return decorated_function


def image_required(f):
    """ image type file is required """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        #test_info_request(request)
        file = request.files['file']
        filename = secure_filename(file.filename)
        name, ext = os.path.splitext(filename)
        
        ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'webp'}
        if ext.replace('.','') not in ALLOWED_EXTENSIONS:
            return jsonify(message="invalid type file "), 400 
        
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
