import logging

from flask import Blueprint, request, jsonify, session
from ..database import db 
from ..services import admin_required_with_exceptions
from ..database.models import User, Cart
from ..services import session_required
from ..services.factories import json_required_with_validation

api_v1_users = Blueprint("api_v1_users", __name__,url_prefix="/api/v1/users")

logging.basicConfig(level=logging.DEBUG)



@api_v1_users.route("/me", methods=["GET"])
@session_required
def me():
    """ GET THE CURRENT USER DATA """
    user = db.session.execute(db.select(User).filter_by(email=session["email"])).scalar()
    if not user:
       return jsonify(message="invalid data"), 400
    return jsonify(user=user.to_dict())



@api_v1_users.route("/<int:user_id>", methods=["GET","PUT", "PATCH", "DELETE"])
@session_required
def update_get_or_delete_user(user_id):
    """ Update/GET/DELETE a user """
    if request.method in ("PUT", "PATH"):
        if "role" in session and session["role"] == "admin":
            user =  db.session.execute(db.select(User).filter_by(id=user_id)).scalar()
        else:
            user = db.session.execute(db.select(User).filter_by(email=session["email"])).scalar()
        if not user:
            return jsonify(message="invalid data")
        data = request.get_json()
        if "firstname" in data:
            user.firstname = data.get("firstname")
        if "lastname" in data:
            user.lastname = data.get("lastname")
        if "password" in data:
            user.password = data.get("password")
        db.session.commit()  
        return jsonify(message="user updated")
    elif request.method == "GET":
        if "role" in session and session["role"] == "admin":
            user =  db.session.execute(db.select(User).filter_by(id=user_id)).scalar()
            if not user:
                return jsonify(message="invalid data"), 400
            return jsonify(user=user.to_dict())
        user =  db.session.execute(db.select(User).filter_by(email=session["email"])).scalar()
        if not user:
            return jsonify(message="invalid data"), 400
        return jsonify(user=user.to_dict())
    else:
        if "role" in session and session["role"] == "admin":
            user =  db.session.execute(db.select(User).filter_by(id=user_id)).scalar()
            if not user:
                return jsonify(message="invalid data"), 400
            db.session.delete(user)
            db.session.commit()
        else:
            user =  db.session.execute(db.select(User).filter_by(email=session["email"])).scalar()
            if not user:
                return jsonify(message="invalid data"), 400
            db.session.delete(user)
            db.session.commit()
        return jsonify(message="user deleted")
   



@api_v1_users.route("/", methods=["POST", "GET"])
#@admin_required_with_exceptions(True, "POST")
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
        user.cart = Cart()
        db.session.add(user)
        db.session.commit()
       
        return jsonify(message="user created with a cart"), 202
    