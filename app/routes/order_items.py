import logging
import os
from pathlib import Path
from flask import Blueprint, request, jsonify, session
from ..database import db 
from ..database.models import OrderItems
from ..services import test_info_request,session_required
 
api_v1_order_items = Blueprint("api_v1_order_items", __name__,url_prefix="/api/v1/order_items")

logging.basicConfig(level=logging.DEBUG)
  
@api_v1_order_items.route("/<int:order_items_id>", methods=["GET","PUT", "DELETE"])
def update_get_or_delete_order_items(order_items_id): 
    """ Update/GET/DELETE a order """
    """ 
    if request.method in ("PUT"):
        order_addresses = db.session.execute(db.select(OrderAddresses).filter_by(id=order_addresses_id )).scalar()
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
        order_addresses =  db.session.execute(db.select(OrderAddresses).filter_by(id=order_addresses_id )).scalar()
        if not order_addresses:
            return jsonify(message="order addresses not found"), 404
         
        return jsonify(order_addresses=order_addresses.to_dict())
    else:
        order_addresses =  db.session.execute(db.select(OrderAddresses).filter_by(id=order_addresses_id )).scalar()
        if not order_addresses:
            return jsonify(message="order addresses not found"), 404
        db.session.delete(order_addresses)
        db.session.commit()
        return jsonify(message="order addresses deleted")
    """
    return jsonify(message="order items updated"), 200    

@api_v1_order_items.route("/", methods=["POST", "GET"])
def get_all_or_create_order_items():
    """ GET ALL ORDER ITEMS OR CREATE A ORDER ITEMS"""
    if request.method == "GET": 
        order_items = db.session.execute(db.select(OrderItems).order_by(OrderItems.id)).scalars()
        return jsonify(order_item=[order_items.to_dict() for order_item in order_items])
    else: 
        """ 
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
            order_addresses = OrderAddresses( 
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
            return jsonify(message="order addresses created"), 201
        except Exception as e:
            logging.error("Error adding order addresses: %s", e)
            db.session.rollback()
            return jsonify(message="error adding order addresses"), 500
        """
        return jsonify(message="order items created"), 201
    