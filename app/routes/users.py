import logging

from flask import Blueprint, request, jsonify, session
from ..database import db 
from ..database.models import User
from ..services import json_required_with_validation, session_required
api_v1_users = Blueprint("api_v1_users", __name__,url_prefix="/api/v1/users")

logging.basicConfig(level=logging.DEBUG)


@api_v1_users.route("/me", methods=["GET"])
@session_required
def me():
    """ GET THE CURRENT USER DATA """
    user = db.session.execute(db.select(User).filter_by(email=session["email"])).scalar()
    if not user:
       return jsonify(message="invalid data")
    return jsonify(user=user.to_dict())

#http://localhost:5000/api/v1/users
@api_v1_users.route("/", methods=["POST", "GET"])
@json_required_with_validation('email', 'password', 'firstname', 'lastname')
def get_all_or_create_user():
    """ GET ALL USERS OR CREATE A USER """
    if request.method == "GET":
        users = db.session.execute(db.select(User).order_by(User.email)).scalars()
        return jsonify(users=[user.to_dict() for user in users])
    else:
        data = request.get_json()
        email =  data.get('email')
        password = data.get('password')
        firstname = data.get('firstname')
        lastname = data.get('lastname')

        ex_user = db.session.execute(db.select(User).filter_by(email=email)).scalar()
        if ex_user:
            return jsonify(message="invalid data"), 400
        
        user = User(firstname=firstname, lastname=lastname, email=email)
        user.password = password
        db.session.add(user)
        db.session.commit()
        return jsonify(message="user created")
    