import os
from pathlib import Path
from werkzeug.utils import secure_filename
from flask import Blueprint, request, jsonify, session, send_from_directory
from ..services import session_required, multipart_form_data_required, unique_filename_required, file_required
from ..database import db
from ..database.models import User
from ..utils import delete_file_in_uploads_folder

UPLOAD_FOLDER=Path(os.getcwd() + "/uploads")
if not UPLOAD_FOLDER.exists():
    os.mkdir(UPLOAD_FOLDER)

static_files=Blueprint("static_files",__name__,url_prefix="/static/files")


@static_files.route('/<filename>', methods=["GET", "DELETE"])
def download_or_delete_file(filename: str):
    """ Download or Delete a File"""
    if request.method == "DELETE":
        if session and 'role' in session:
            user = db.session.execute(db.select(User).filter_by(email=session["email"])).scalar()
            if not user:
                return jsonify(message="invalid data"), 400   
            if user.photo_name and isinstance(user.photo_name, str):
                if not (user.photo_name == filename):
                    return jsonify(messafe="invalid filename"), 400
                delete_file_in_uploads_folder(user.photo_name)
                user.photo_name=None
                db.session.commit()
                return jsonify(message="file deleted and user updated")
        return jsonify(message="authorized action"), 401
    if request.method == "GET":
        """ download a file (-> client) """
        return send_from_directory(UPLOAD_FOLDER, filename)


@static_files.route('/upload', methods=['POST'])
@session_required
@multipart_form_data_required
@file_required
@unique_filename_required
def upload_file(unique_name):
    """ uploads a file (-> server) """
    file = request.files['file']
    file.save(os.path.join(UPLOAD_FOLDER, unique_name))
    if "role" in session and (session["role"] == "user" or session["role"] == "premium" or session["role"] == "admin"):
        user = db.session.execute(db.select(User).filter_by(email=session["email"])).scalar()
        user.photo_name = unique_name
        db.session.commit()
        return jsonify(message="file saved"), 200
    return jsonify(message="invalid data"), 400
