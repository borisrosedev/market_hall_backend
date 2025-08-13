from flask import Blueprint, jsonify, session
from ..services import session_required
from ..database import db
from ..database.models import Cart

api_v1_carts = Blueprint("api_v1_cart", __name__, url_prefix="/api/v1/carts")


@api_v1_carts.route("/", methods=["GET"])
def get_all_carts():
    carts = db.session.execute(db.select(Cart).order_by(Cart.id)).scalars()
    return jsonify(carts = [cart.to_dict() for cart in carts])


@api_v1_carts.route("/me", methods=["GET"])
@session_required
def get_current_user_cart():
    """ Get the current user cart """ 
    cart = db.session.execute(db.select(Cart).filter_by(user_id=session["user_id"])).scalar()
    if not cart:
        return jsonify(message="invalid data"), 400
    return jsonify(cart=cart.to_dict())


@api_v1_carts.route("/items", methods=["POST"])
@session_required
def add_cart_item():
   return jsonify(message="cart item added")