import logging

from flask import Blueprint, request, jsonify, session
from ..database import db 
from ..services import json_required_with_validation, session_required, admin_required_with_exceptions
api_v1_products = Blueprint("api_v1_products", __name__,url_prefix="/api/v1/products")

logging.basicConfig(level=logging.DEBUG)

# api_v1_products.before_request() ( check to see if you put the decorator in before requrest )

# route to handle the create of a new product 

# route to handle the getting of all products

# route to handler the getting of one product

# route to  handle the update of a product 

# route to handle the deletion of a product 
