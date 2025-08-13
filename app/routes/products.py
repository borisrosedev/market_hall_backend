import logging
import uuid
from pathlib import Path 
import os
from datetime import datetime as dt
from flask import Blueprint, request, jsonify, session
from ..database import db 
from ..database.models import Product, Tag, TagProduct
from werkzeug.utils import secure_filename
from ..services import session_required, multipart_form_data_with_specific_extension_file_and_keys, unique_filename_required



UPLOAD_FOLDER=Path(os.getcwd() + "/uploads")

api_v1_products = Blueprint("api_v1_products", __name__,url_prefix="/api/v1/products")
logging.basicConfig(level=logging.DEBUG)


@api_v1_products.route("/", methods=["POST", "GET"])
@multipart_form_data_with_specific_extension_file_and_keys(
    ["png","jpg","webp", "gif","jpeg"],
    ["description", "name","price", "quantity", "tags"]
)
@unique_filename_required
def get_all_or_create_product(unique_name:str):
    """ GET ALL PRODUCTS OR CREATE A PRODUCT """      
    if request.method == "GET":
        products = db.session.execute(db.select(Product)).scalars()     
        return jsonify(products=[product.to_dict() for product in products])
    description = request.form.get('description')
    name = request.form.get('name')
    is_available= request.form.get('is_available') if request.form.get('is_available') else True
    price= request.form.get('price')
    tags = request.form.get('tags')
    quantity= request.form.get('quantity')
    file = request.files["file"]
    file.save(os.path.join(UPLOAD_FOLDER, unique_name))
    try:
        product = Product(
            description=description,
            is_available=is_available,
            name=name,
            photo_name=unique_name,
            price=price,
            quantity=quantity,
        )
        for tag_name in tags.split(','):
            tag = Tag(name=tag_name.strip())
            tag_link = TagProduct(tag=tag)
            product.tag_links.append(tag_link)
        db.session.add(product)
        db.session.commit()
        return jsonify(message="product created"), 202
    except Exception as e:
        logging.error("Error adding product: %s", e)
        db.session.rollback()
        return jsonify(message="error adding product"), 500


@api_v1_products.route("/<int:product_id>", methods=["PUT"])
def update_product(product_id):   
    """ UPDATE A PRODUCT """  
    data = request.get_json()
    product = db.session.execute(db.select(Product).filter_by(id=product_id)).scalar()
    if not product:
        return jsonify(message="product not found"), 404
    # Update fields if they are provided in the request
    for key, value in data.items():
        if hasattr(product, key):
            setattr(product, key, value)
    db.session.commit()
    return jsonify(message="product updated")


@api_v1_products.route("/<int:product_id>", methods=["DELETE"])
def get_delete_product(product_id):
    """  DELETE A PRODUCT """  
    product = db.session.execute(db.select(Product).filter_by(id=product_id)).scalar()
    if not product:
        return jsonify(message="product not found"), 404
    db.session.delete(product)
    db.session.commit()
    return jsonify(message="product deleted")


@api_v1_products.route("/<int:product_id>", methods=["GET"])
def get_by_product(product_id):
    """ GET A PRODUCT   """   
    product = db.session.execute(db.select(Product).filter_by(id=product_id)).scalar()
    if not product:
        return jsonify(message="product not found"), 404
    return jsonify(product=product.to_dict())
   
