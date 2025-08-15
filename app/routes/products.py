import logging
import uuid
import os
from pathlib import Path 
from flask import Blueprint, request, jsonify
from ..database import db 
from ..database.models import Product
from ..services import multipart_form_data_with_specific_extension_file_and_keys, unique_filename_required,test_info_request, admin_required_with_exceptions
from .helpers import tags_helper


UPLOAD_FOLDER=Path(os.getcwd() + "/uploads")

api_v1_products = Blueprint("api_v1_products", __name__,url_prefix="/api/v1/products")
logging.basicConfig(level=logging.DEBUG)




@api_v1_products.route("/", methods=["POST", "GET"])
@admin_required_with_exceptions(True, "GET")
@multipart_form_data_with_specific_extension_file_and_keys(
    ["png","jpg","webp", "gif","jpeg"],
    ["description", "name","price", "quantity", "tags"]
)
@unique_filename_required
def get_all_delete_all_or_create_product(unique_name:str=None):
    """ GET ALL PRODUCTS OR CREATE A PRODUCT """      
    if request.method == "GET":
        products = db.session.execute(db.select(Product)).scalars()    
        return jsonify(products=[product.to_dict() for product in products])
    if request.method == "DELETE":
        db.session.query(Product).delete()
        db.session.commit()
        return jsonify(message="all products deleted")
    description = request.form.get('description') 
    name = request.form.get('name')
    is_available= request.form.get('is_available') if request.form.get('is_available') else True
    price= request.form.get('price')
    tags = request.form.get('tags')
    quantity= request.form.get('quantity')
    file = request.files["file"]
    file.save(os.path.join(UPLOAD_FOLDER, unique_name))
    test_info_request(request)
    try:
        product = Product(
            description=description,
            is_available=is_available, 
            name=name,
            photo_name=unique_name,
            price=price,
            quantity=quantity,
        )
        tags_helper(product=product,tags=tags)
        db.session.add(product)
        db.session.commit()
        return jsonify(message="product created"), 201
    except Exception as e:
        logging.error("Error adding product: %s", e)
        db.session.rollback()
        return jsonify(message="error adding product"), 500



@api_v1_products.route("/<int:product_id>", methods=["DELETE", "GET", "PUT", "PATCH"])
@admin_required_with_exceptions(True, "GET")
@unique_filename_required
def get_update_delete_one_product(product_id, unique_name:str=None):
    if request.method in ("PUT", "PATCH"): 
        product = db.session.execute(db.select(Product).filter_by(id=product_id)).scalar()
        if not product:
            return jsonify(message="product not found"), 404
        if unique_name:
            product.photo_name = unique_name
            file = request.files['file']
            file.save(os.path.join(UPLOAD_FOLDER, unique_name))

        description = request.form.get('description') 
        name = request.form.get('name')
        is_available= request.form.get('is_available') if request.form.get('is_available') else True
        price= request.form.get('price')
        tags = request.form.get('tags')
        quantity= request.form.get('quantity')
        
        if description:
            product.description = description
        if name: 
            product.name = name 
        if is_available:
            product.is_available = is_available
        if price:
            product.price = price
        if quantity:
            product.quantity = quantity
        if tags:
            tags_helper(product=product,tags=tags)

        db.session.commit()
        return jsonify(message="product updated"), 200

    if request.method == "GET": 
        product = db.session.execute(db.select(Product).filter_by(id=product_id)).scalar()
        if not product:
            return jsonify(message="product not found"), 404
        return jsonify(product=product.to_dict())
    
    if request.method == "DELETE":
        product = db.session.execute(db.select(Product).filter_by(id=product_id)).scalar()
        if not product:
            return jsonify(message="product not found"), 404
        db.session.delete(product)
        db.session.commit()
        return jsonify(message="product deleted")

