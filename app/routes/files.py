import os
from pathlib import Path
from werkzeug.utils import secure_filename
from flask import Blueprint, request, jsonify, session, send_from_directory
from ..services import session_required,file_required ,deco_test, unique_filename_required
from ..database import db
from ..database.models import User

UPLOAD_FOLDER=Path(os.getcwd() + "/uploads")
if not UPLOAD_FOLDER.exists():
    os.mkdir(UPLOAD_FOLDER)
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'webp'}

static_files=Blueprint("static_files",__name__,url_prefix="/static/files")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@static_files.route('/<filename>', methods=["GET"])
@deco_test
def download_file(filename: str):
    """ download a file (-> client) """
    return send_from_directory(UPLOAD_FOLDER, filename)


@static_files.route('/upload', methods=['POST'])
@session_required
@unique_filename_required
def upload_file(unique_name):
    """ uploads a file (-> server) """
    file = request.files['file']
    file.save(os.path.join(UPLOAD_FOLDER, unique_name))
    if "role" in session and (session["role"] == "user" or session["role"] == "premium"):
        user = db.session.execute(db.select(User).filter_by(email=session["email"])).scalar()
        user.photo_name = unique_name
        db.session.commit()
        return jsonify(message="file saved"), 200
    return jsonify(message="invalid data"), 400