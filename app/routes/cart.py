from flask import Blueprint, jsonify, request, session
from ..services import session_required
from ..database import db
from ..database.models import Cart

api_v1_cart = Blueprint("api_v1_cart", __name__, url_prefix="/api/v1/cart")


@api_v1_cart.route("/", methods=["GET"])
@session_required
def get_current_user_cart():
    """ Get the current user cart """ 
    cart = db.session.execute(db.select(Cart).filter_by(user_id=session["user_id"])).scalar()
    return jsonify(cart=cart.to_dict())


@api_v1_cart.route("/items", methods=["POST"])
@session_required
def add_cart_item():
   return jsonify(message="cart item added")