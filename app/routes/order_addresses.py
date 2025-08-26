import logging
import os
from pathlib import Path
from flask import Blueprint, request, jsonify, session
from ..database import db 
from ..database.models import OrderAddresses
from ..services import test_info_request


api_v1_order_addresses = Blueprint("api_v1_order_addresses", __name__,url_prefix="/api/v1/order_addresses")

logging.basicConfig(level=logging.DEBUG)
 

@api_v1_order_addresses.route("/<int:order_addresses_id>", methods=["GET","PUT", "DELETE"])
def update_get_or_delete_order_addresses(order_addresses_id): 
    """ Update/GET/DELETE a order """
    if request.method in ("PUT"):
        order_addresses = db.session.execute(db.select(OrderAddresses).filter_by(id=order_addresses_id )).scalar()
        if not order_addresses:
            return jsonify(message="order addresses not found"), 404
        test_info_request(request) 
        data = request.get_json()
        """ 
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
        """
        return jsonify(message="order updated"), 200
    
         
    elif request.method == "GET":
        order_addresses =  db.session.execute(db.select(OrderAddresses).filter_by(id=id )).scalar()
        if not order:
            return jsonify(message="order addresses not found"), 404
         
        return jsonify(order_addresses=order_addresses.to_dict())
    else:
        order_addresses =  db.session.execute(db.select(OrderAddresses).filter_by(id=id )).scalar()
        if not order_addresses:
            return jsonify(message="order addresses not found"), 404
        db.session.delete(order_addresses)
        db.session.commit()
        return jsonify(message="order addresses deleted")
 

@api_v1_order_addresses.route("/", methods=["POST", "GET"])
def get_all_or_create_order_addresses():
    """ GET ALL ORDER ADDRESSES OR CREATE A ORDER ADDRESS"""
    if request.method == "GET": 
        orders = db.session.execute(db.select(OrderAddresses).order_by(OrderAddresses.id)).scalars()
        return jsonify(orders=[order.to_dict() for order in orders])
    else: 
        data = request.get_json()
        """ 
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
        """
        return jsonify(message="order adress created"), 201  
    