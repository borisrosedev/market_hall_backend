import logging
import os
from pathlib import Path
from flask import Blueprint, request, jsonify, session
from ..database import db 
#from ..services import admin_required_with_exceptions
from ..database.models import  Orders
from ..services import test_info_request
#from ..services.factories import json_required_with_validation
#UPLOAD_FOLDER=Path(os.getcwd() + "/uploads")


api_v1_orders = Blueprint("api_v1_orders", __name__,url_prefix="/api/v1/orders")

logging.basicConfig(level=logging.DEBUG)
 

@api_v1_orders.route("/<int:order_id>", methods=["GET","PUT", "PATCH", "DELETE"])
#@session_required 
def update_get_or_delete_order(): #user_id,unique_name: str = None):
    """ Update/GET/DELETE a order """
    """
    if request.method in ("PUT", "PATH"):
        if "role" in session and session["role"] == "admin":
            user =  db.session.execute(db.select(User).filter_by(id=user_id)).scalar()
        else:
            user = db.session.execute(db.select(User).filter_by(email=session["email"])).scalar()
        if not user:
            return jsonify(message="invalid data")
        
        if request.is_json: 
            data = request.get_json()
            if "firstname" in data:
                user.firstname = data.get("firstname")
            if "lastname" in data:
                user.lastname = data.get("lastname")
            if "email" in data:
                user.email = data.get("email")
            if "password" in data:
                user.password = data.get("password")

            if session["role"] == "admin":
                if "role" in data:
                    user.role = data.get("role")
        else:
            if request.form.get('firstname'):
                user.firstname = request.form.get('firstname')
            if request.form.get('lastname'):
                user.lastname = request.form.get('lastname')
            if request.form.get('email'):
                user.email = request.form.get('email')
            if request.form.get('password'):
                user.password = data.get("password")
            if session["role"] == "admin":
                if  request.form.get('role'):
                    user.role = request.form.get('role')
 
            file = request.files['file']
  
            logging.info(file)

            file.save(os.path.join(UPLOAD_FOLDER, unique_name))
            user = db.session.execute(db.select(User).filter_by(email=session["email"])).scalar()
            user.photo_name = unique_name
 

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
    """ 
    return jsonify(message="order test")
    


@api_v1_orders.route("/", methods=["POST", "GET"])
def get_all_or_create_order():
    """ GET ALL ORDERS OR CREATE A ORDER """
    if request.method == "GET": 
        orders = db.session.execute(db.select(Orders).order_by(Orders.id)).scalars()
        return jsonify(orders=[order.to_dict() for order in orders])
    else: 
        data = request.get_json()
        user_id =  data.get('user_id')
        amounts_cents =data.get('amounts_cents')
        currency = data.get('currency')
        status = data.get('status') 
        test_info_request(request)
        try:
            order = Orders(
                user_id=user_id,
                amounts_cents= amounts_cents,
                currency=currency, 
                status=status, 
            )
           
            db.session.add(order)
            db.session.commit()
            return jsonify(message="order created"), 201
        except Exception as e:
            logging.error("Error adding order: %s", e)
            db.session.rollback()
            return jsonify(message="error adding order"), 500

          
    