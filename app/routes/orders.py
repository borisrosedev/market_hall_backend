import logging
import os
from pathlib import Path
from flask import Blueprint, request, jsonify, session
from ..database import db 
from ..database.models import  Orders
from ..services import test_info_request


api_v1_orders = Blueprint("api_v1_orders", __name__,url_prefix="/api/v1/orders")

logging.basicConfig(level=logging.DEBUG)
 

@api_v1_orders.route("/<int:order_id>", methods=["GET","PUT", "DELETE"])
#@session_required 
def update_get_or_delete_order(order_id): 
    """ Update/GET/DELETE a order """
    if request.method in ("PUT"):
        order = db.session.execute(db.select(Orders).filter_by(id=order_id )).scalar()
        if not order:
            return jsonify(message="order not found"), 404
        #test_info_request(request) 
        data = request.get_json()
        user_id = data.get('user_id') 
        amounts_cents= data.get('amounts_cents')  
        currency= data.get('currency')
        status = data.get('status') 
         
        if user_id:
            order.user_id = user_id
        if amounts_cents:
            order.amounts_cents = amounts_cents
        if currency:
            order.currency = currency  
        if status:
            order.status = status   
         
        db.session.commit()
        return jsonify(message="order updated"), 200
    
         
    elif request.method == "GET":
        order =  db.session.execute(db.select(Orders).filter_by(id=order_id )).scalar()
        if not order:
            return jsonify(message="order not found"), 404
         
        return jsonify(order=order.to_dict())
    else:
        order =  db.session.execute(db.select(Orders).filter_by(id=order_id )).scalar()
        if not order:
            return jsonify(message="order not found"), 404
        db.session.delete(order)
        db.session.commit()
        return jsonify(message="order deleted")
 

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

          
    