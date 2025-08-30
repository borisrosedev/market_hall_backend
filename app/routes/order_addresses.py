import logging
import os
from pathlib import Path
from flask import Blueprint, request, jsonify, session
from ..database import db 
from ..database.models import OrderAddresse
from ..services import test_info_request,session_required
 
api_v1_order_addresses = Blueprint("api_v1_order_addresses", __name__,url_prefix="/api/v1/order_addresses")

logging.basicConfig(level=logging.DEBUG)
  
@api_v1_order_addresses.route("/<int:order_addresses_id>", methods=["GET","PUT", "DELETE"])
def update_get_or_delete_order_addresses(order_addresses_id): 
    """ Update/GET/DELETE a order """
    if request.method in ("PUT"):
        order_addresses = db.session.execute(db.select(OrderAddresse).filter_by(id=order_addresses_id )).scalar()
        if not order_addresses:
            return jsonify(message="order addresses not found"), 404
        #test_info_request(request) 
        data = request.get_json() 
        order_id= data.get('order_id') 
        type = data.get('type')  
        full_name= data.get('full_name')
        line1 = data.get('line1') 
        line2 = data.get('line2') 
        city= data.get('city') 
        postal_code= data.get('postal_code') 
        country= data.get('country') 
        phone= data.get('phone') 

        if order_id:
            order_addresses.order_id = order_id
        if type:
            order_addresses.type = type
        if full_name:
            order_addresses.full_name = full_name  
        if line1:
            order_addresses.line1 = line1   
        if line2:
            order_addresses.line2 = line2
        if city:
            order_addresses.city = city
        if postal_code:
            order_addresses.postal_code = postal_code
        if country:
            order_addresses.country = country
        if phone:
            order_addresses.phone = phone
        db.session.commit()
        
        return jsonify(message="order addresses updated"), 200    
    elif request.method == "GET":
        order_addresses =  db.session.execute(db.select(OrderAddresse).filter_by(id=order_addresses_id )).scalar()
        if not order_addresses:
            return jsonify(message="order addresses not found"), 404
         
        return jsonify(order_addresses=order_addresses.to_dict())
    else:
        order_addresses =  db.session.execute(db.select(OrderAddresse).filter_by(id=order_addresses_id )).scalar()
        if not order_addresses:
            return jsonify(message="order addresses not found"), 404
        db.session.delete(order_addresses)
        db.session.commit()
        return jsonify(message="order addresses deleted")
 

@api_v1_order_addresses.route("/", methods=["POST", "GET"])
def get_all_or_create_order_addresses():
    """ GET ALL ORDER ADDRESSES OR CREATE A ORDER ADDRESS"""
    if request.method == "GET": 
        order_addresses = db.session.execute(db.select(OrderAddresse).order_by(OrderAddresse.id)).scalars()
        return jsonify(order_addresses=[order_address.to_dict() for order_address in order_addresses])
    else: 
        data = request.get_json() 
        order_id= data.get('order_id') 
        type = data.get('type')   
        full_name= data.get('full_name')
        line1 = data.get('line1') 
        line2 = data.get('line2') 
        city= data.get('city') 
        postal_code= data.get('postal_code') 
        country= data.get('country') 
        phone= data.get('phone') 
        
        try:
            order_addresses = OrderAddresse( 
                order_id = order_id ,
                type = type, 
                full_name = full_name ,  
                line1 = line1 ,  
                line2 = line2 ,
                city = city ,
                postal_code = postal_code ,
                country = country, 
                phone = phone
            )
           
            db.session.add(order_addresses)
            db.session.commit()
            return jsonify(message="order addresse created"), 201
        except Exception as e:
            logging.error("Error adding order addresse: %s", e)
            db.session.rollback()
            return jsonify(message="error adding order addresse"), 500
          
    