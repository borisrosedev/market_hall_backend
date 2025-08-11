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
# @session_required
@api_v1_products.route("/", methods=["POST", "GET"])
def get_all_or_create_product():
    """ GET ALL PRODUCTS OR CREATE A PRODUCT """     
    
    if request.method == "GET":
        products = db.session.execute(db.select(Product)).scalars().all()     
        #prd = db.select(Product)
        #products = db.session.execute(prd).scalars() 
        #products = db.session.execute(db.select(Product).order_by(Product.id)).scalars()
        return jsonify(products=[product.to_dict() for product in products])
    else:
        
        data = request.get_json()
        #id =  data.get('id')

        
        required_fields = ['description', 'name', 'photo_name', 'price', 'quantity']
        for field in required_fields:
            if not data.get(field):
                return jsonify(message=f"Missing required field: {field}"), 400
            
        description = data.get('description')
        is_available= data.get('is_available')
        name= data.get('name')
        photo_name= data.get('photo_name')
        price= data.get('price') 
        quantity= data.get('quantity')
        #created_at= data.get('created_at')
        #updated_at= data.get('updated_at')

        ##try:
        #    ex_product = db.session.execute(db.select(Product).filter_by(id=id)).scalar()
        #    if ex_product:
        #        return jsonify(message="invalid data"), 400
        #except Exception as e:
        #    logging.error(f"Error checking existing product: {e}")  
        #    return jsonify(message="error checking existing product"), 500

        
        
        
        try :

            product = Product(
                description=description,
                is_available=is_available,
                name=name,
                photo_name=photo_name,
                price=price,
                quantity=quantity,
             
             )
            logging.debug(f"Creating product: {product}")

            db.session.add(product)
            db.session.commit()
        except Exception as e:
            logging.error(f"Error adding product: {e}")
            db.session.rollback()
            return jsonify(message="error adding product"), 500
         
        return jsonify(message="product created")
    
 

# route to  handle the update of a product 
@session_required
@api_v1_products.route("/update", methods=["POST"])
def update_product():   
    """ UPDATE A PRODUCT """  
    data = request.get_json()
    product_id = data.get("id")
    if not product_id:
        return jsonify(message="product id is required"), 400
    
    product = db.session.execute(db.select(Product).filter_by(id=product_id)).scalar()
    if not product:
        return jsonify(message="product not found"), 404
    
    # Update fields if they are provided in the request
    for key, value in data.items():
        if hasattr(product, key):
            setattr(product, key, value)
    
    db.session.commit()
    return jsonify(message="product updated")

# route to handle the deletion of a product 
@session_required
@api_v1_products.route("/delete", methods=["POST"])
def get_delete_product():
    """  DELETE A PRODUCT """  
    product_id = request.args.get("id")
    if not product_id:
        return jsonify(message="product id is required"), 400
    
    product = db.session.execute(db.select(Product).filter_by(id=product_id)).scalar()
    if not product:
        return jsonify(message="product not found"), 404
    
    db.session.delete(product)
    db.session.commit()
    return jsonify(message="product deleted")

# route to handler the getting of one product
@session_required
@api_v1_products.route("/getBy", methods=[  "GET"])
def get_by_product():
    """ GET A PRODUCT   """  
    product_id = request.args.get("id")
    if not product_id:
        return jsonify(message="product id is required"), 400
    
    product = db.session.execute(db.select(Product).filter_by(id=product_id)).scalar()
    if not product:
        return jsonify(message="product not found"), 404
    
    return jsonify(product=product.to_dict())
    
     
