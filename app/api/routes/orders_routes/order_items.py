import logging
import os
from pathlib import Path
from sqlite3 import IntegrityError
from flask import Blueprint, request, jsonify, session
from ....database import db 
from ....models.db_models.order import Order 
from ....models.db_models.order_item import OrderItem
from ....models.db_models.order_addresse import OrderAddresse
from ...services.decorators.auth import session_required
 
api_v1_order_items = Blueprint("api_v1_order_items", __name__,url_prefix="/api/v1/order_items")

logging.basicConfig(level=logging.DEBUG)
  
@api_v1_order_items.route("/<int:order_items_id>", methods=["GET","PUT", "DELETE"])
def update_get_or_delete_order_items(order_items_id): 
    """ Update/GET/DELETE a order items""" 
    if request.method in ("PUT", "DELETE"):
        return jsonify(message="operation not authorized on order items"), 200    
    elif request.method == "GET":
        order_items =  db.session.execute(db.select(OrderItem).filter_by(id=order_items_id )).scalar()
        if not order_items:
            return jsonify(message="order items not found"), 404
         
        return jsonify(order_items=order_items.to_dict())
    
       

@api_v1_order_items.route("/", methods=["POST", "GET"])
def get_all_or_create_order_items():
    """ GET ALL ORDER ITEMS OR CREATE A ORDER ITEMS"""
    if request.method == "GET": 
        order_items = db.session.execute(db.select(OrderItem).order_by(OrderItem.id)).scalars()
        return jsonify(order_items=[order_item.to_dict() for order_item in order_items])
    else: 
        data = request.get_json() 
        order_id= data.get('order_id') 
        product_id= data.get('product_id') 
        
        order = db.session.get(Order, order_id)
        if not order:
            return jsonify(message=f"Order with id {order_id} does not exist"), 400
         
        product = db.session.get(Product, product_id)
        if not product:
            return jsonify(message=f"Product with id {product_id} does not exist"), 400
    
        sku = data.get('sku')  
        product_name= data.get('product_name')
        unit_price_cents = data.get('unit_price_cents') 
        quantity = data.get('quantity') 
        subtotal_cents= data.get('subtotal_cents') 
        tax_cents= data.get('tax_cents') 
        discount_cents= data.get('discount_cents') 
        total_cents= data.get('total_cents') 
        currency= data.get('currency') 
        variant_json= data.get('variant_json', {}) 
        metadata_json= data.get('metadata_json', {}) 
    
        created_at= data.get('created_at') 
        
        try:
            order_items = OrderItem( 
                order_id = order_id ,
                product_id = product_id, 
                sku = sku ,  
                product_name = product_name ,  
                unit_price_cents = unit_price_cents ,
                quantity = quantity ,
                subtotal_cents = subtotal_cents ,
                tax_cents = tax_cents, 
                discount_cents = discount_cents,
                total_cents = total_cents, 
                currency = currency, 
                variant_json = variant_json, 
                metadata_json = metadata_json, 
                created_at = created_at 
            )
            db.session.add(order_items)
            db.session.commit()
            return jsonify(message="order item created"), 201
        
        except IntegrityError as e:
            logging.error("Database integrity error: %s", e)
            db.session.rollback()
            return jsonify(message="Invalid data or duplicate entry"), 400
        except Exception as e:
            logging.error("Error adding order item: %s", e)
            db.session.rollback()
            return jsonify(message="error adding order item"), 500
        
    