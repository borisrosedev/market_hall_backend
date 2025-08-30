import logging
import os
from pathlib import Path
from flask import Blueprint, request, jsonify
from ..database import db
from ..database.models import Product, Tag
from ..services import multipart_form_data_with_specific_extension_file_and_keys, unique_filename_required,test_info_request, admin_required_with_exceptions, admin_required
from .helpers import tags_helper
from ..utils import delete_file_in_uploads_folder, to_bool, to_int, to_float

UPLOAD_FOLDER=Path(os.getcwd() + "/uploads")

api_v1_products = Blueprint("api_v1_products", __name__,url_prefix="/api/v1/products")
logging.basicConfig(level=logging.DEBUG)




@api_v1_products.route("/", methods=["POST", "GET"])
@admin_required_with_exceptions(True, "GET")
@multipart_form_data_with_specific_extension_file_and_keys(
    ["png","jpg","webp", "gif","jpeg"],
    ["description", "name","price_cents", "quantity", "tags"]
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
    price_cents= request.form.get('price_cents')
    tags = request.form.get('tags')
    quantity= request.form.get('quantity')
    sku= request.form.get('sku')
    file = request.files["file"]
    file.save(os.path.join(UPLOAD_FOLDER, unique_name))
    test_info_request(request)
    try:
        product = Product(
            description=description,
            is_available=is_available, 
            name=name,
            photo_name=unique_name,
            price_cents=price_cents,
            quantity=quantity,
            sku=sku,
        )
        tags_helper(product=product,tags=tags)
        db.session.add(product)
        db.session.commit()
        return jsonify(message="product created"), 201
    except Exception as e:
        logging.error("Error adding product: %s", e)
        db.session.rollback()
        return jsonify(message="error adding product"), 500


@api_v1_products.route("/<int:product_id>/tags/<int:tag_id>", methods=["DELETE"])
@admin_required
def delete_one_product_tag(product_id, tag_id):
    product = db.session.execute(db.select(Product).filter_by(id=product_id)).scalar()
    if not product:
        return jsonify(message="invalid product id"), 400

    tag = db.session.execute(db.select(Tag).filter_by(id=tag_id)).scalar()
    if not tag:
        return jsonify(message="invalid tag id"), 400

    if tag not in product.tags:
        return jsonify(message=f"product {product_id} does not have tag {tag_id}"), 400

    product.tags.remove(tag)
    db.session.commit()

    return jsonify(message="tag removed"), 200

@api_v1_products.route("/<int:product_id>", methods=["DELETE", "GET", "PUT", "PATCH"])
@admin_required_with_exceptions(True, "GET")
@unique_filename_required
def get_update_delete_one_product(product_id, unique_name: str = None):
    if request.method in ("PUT", "PATCH"):
        product = db.session.execute(
            db.select(Product).filter_by(id=product_id)
        ).scalar_one_or_none()
        if not product:
            return jsonify(message="product not found"), 404


        if request.is_json:
            data = request.get_json()
            description = data.get("description")
            name = data.get("name")
            is_available = data.get("is_available") if "is_available" in data else None
            price_cents = data.get("price_cents")
            tags = data.get("tags")
            quantity = data.get("quantity")
            sku = data.get("sku")
        else:
            if unique_name:
                if isinstance(product.photo_name, str):
                    delete_file_in_uploads_folder(product.photo_name)
                product.photo_name = unique_name
                file = request.files["file"]
                file.save(os.path.join(UPLOAD_FOLDER, unique_name))

            description = request.form.get("description")
            name = request.form.get("name")
            is_available = request.form.get("is_available") if "is_available" in request.form else None
            price_cents = request.form.get("price_cents")
            tags = request.form.get("tags")
            quantity = request.form.get("quantity")
            sku = request.form.get("sku")

        if description is not None:
            product.description = description
        if name is not None:
            product.name = name
        if is_available is not None:
            val = to_bool(is_available)
            if val is not None:
                product.is_available = val
        if price_cents is not None:
            val = to_float(price_cents)
            if val is not None:
                product.price_cents = val
        if quantity is not None:
            val = to_int(quantity)
            if val is not None:
                product.quantity = val
        if sku is not None:
            val = to_int(sku)
            if val is not None:
                product.sku = val        
        if tags is not None:
            tags_helper(product=product, tags=tags)

        db.session.commit()
        return jsonify(message="product updated"), 200

    if request.method == "GET":
        product = db.session.execute(db.select(Product).filter_by(id=product_id)).scalar_one_or_none()
        if not product:
            return jsonify(message="product not found"), 404
        return jsonify(product=product.to_dict())

    if request.method == "DELETE":
        product = db.session.execute(db.select(Product).filter_by(id=product_id)).scalar_one_or_none()
        if not product:
            return jsonify(message="product not found"), 404
        if isinstance(product.photo_name, str):
            delete_file_in_uploads_folder(product.photo_name)
        db.session.delete(product)
        db.session.commit()
        return jsonify(message="product deleted")
