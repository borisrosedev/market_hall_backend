import logging

from flask import Blueprint, request, jsonify, session
from ..database import db 
from ..services import admin_required_with_exceptions
from ..database.models import Product
from ..services import json_required_with_validation, session_required
api_v1_products = Blueprint("api_v1_products", __name__,url_prefix="/api/v1/products")

logging.basicConfig(level=logging.DEBUG)

# api_v1_products.before_request() ( check to see if you put the decorator in before requrest )

# route to handle the create of a new product  
# route to handle the getting of all products
#  @session_required
@api_v1_products.route("/", methods=["POST", "GET"])
#@admin_required_with_exceptions(True, "POST")
#@json_required_with_validation('id','name' )
def get_all_or_create_product():
    """ GET ALL PRODUCTS OR CREATE A PRODUCT """     
    print ("bgu request method", request.method)
    if request.method == "GET":
        products = db.session.execute(db.select(Product).order_by(Product.id)).scalars()
        return jsonify(product=[product.to_dict() for product in products])
    else:
        data = request.get_json()
        id =  data.get('id')
        description = data.get('description')
        is_available= data.get('is_available')
        name= data.get('name')
        photo_name= data.get('photo_name')
        price= data.get('price') 
        quantity= data.get('quantity')
        created_at= data.get('created_at')
        updated_at= data.get('updated_at')
       

        ex_product = db.session.execute(db.select(Product).filter_by(id=id)).scalar()
        if ex_product:
            return jsonify(message="invalid data"), 400
        
        product = Product(
            id=id,
            description=description,
            is_available=is_available,
            name=name,
            photo_name=photo_name,
            price=price,
            quantity=quantity,
            created_at=created_at,
            updated_at=updated_at
        )
         
        db.session.add(product)
        db.session.commit()
        return jsonify(message="product created")
    


# route to handler the getting of one product

# route to  handle the update of a product 

# route to handle the deletion of a product 
