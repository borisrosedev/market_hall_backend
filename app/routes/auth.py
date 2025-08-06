from flask import session, Blueprint, jsonify, request
from ..services import session_required, json_required_with_keys
from ..database import db 
from ..database.models import User

api_v1_auth = Blueprint("api_v1_auth", __name__, url_prefix="/api/v1/auth")


@api_v1_auth.route('/login', methods=["POST"])
@json_required_with_keys('email', 'password')
def login():
    """ Log in the user """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = db.session.execute(db.select(User).filter_by(email=email)).scalar()

    if not user:
        return jsonify(message="invalid data")
    
    session["email"] = user.email 
    session["role"] = user.role.value
    session.permanent = True

    return jsonify(message="session started")


@api_v1_auth.route('/logout', methods=["GET"])
@session_required
def logout():
    """ Log out the user """
    session.pop('email', None)
    session.pop('role', None)
    return jsonify(message="session end")