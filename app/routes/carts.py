from flask import Blueprint, jsonify, session, request
from ..services import session_required, admin_required
from ..database import db
from ..database.models import Cart, Product, User, CartProduct
from ..utils import to_int

api_v1_carts = Blueprint("api_v1_cart", __name__, url_prefix="/api/v1/carts")


@api_v1_carts.route("/", methods=["GET"])
@admin_required
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



@api_v1_carts.route("/<int:cart_id>/items", methods=["DELETE"])
@session_required
def delete_all_items_from_cart(cart_id):
    # ℹ️ You should create a decorator that checks if the user exists and returns it
    user = db.session.execute(db.select(User).filter_by(email=session["email"])).scalar_one_or_none()
    if not user:
        return jsonify(message="invalid data"), 400
    # ℹ️ You should create a decorator that checks if the cart exists and returns it
    cart = db.session.execute(db.select(Cart).filter_by(id=user.cart.id)).scalar_one_or_none()
    if not cart:
        return jsonify(message="invalid cart id"), 400
    
    cart.items.clear()
    db.session.commit()
    return jsonify(message="all items deleted from cart")


@api_v1_carts.route("/<int:cart_id>/items/<int:item_id>", methods=["GET", "DELETE"])
@session_required
def add_cart_item_or_update_quantity(cart_id, item_id):
    args=request.args

    # ℹ️ You should create a decorator that checks if the user exists and returns it
    user = db.session.execute(db.select(User).filter_by(email=session["email"])).scalar_one_or_none()
    if not user:
        return jsonify(message="invalid data"), 400
    
    # ℹ️ You should create a decorator that checks if the cart exists and returns it
    cart = db.session.execute(db.select(Cart).filter_by(id=user.cart.id)).scalar_one_or_none()
    if not cart:
        return jsonify(message="invalid cart id"), 400
    
    # ℹ️ You should create a decorator that checks if the products exists and returns it
    product = db.session.execute(db.select(Product).filter_by(id=item_id)).scalar_one_or_none()
    if not product:
        return jsonify(message="invalid product id")

    if request.method == "GET":
        qty = to_int(args.get("quantity"), default=1)
        # ➡️ Check if the product already is in the user's cart
        for cart_item in cart.items:
            if cart_item.product_id == item_id:
                # ✅ if exists, we only change the quantity value
                if qty is not None:
                    cart_item.quantity = qty
                    db.session.commit()
                    return jsonify(message="cart item quantity updated")          
        # ➡️ Case it does not already exist in the user's cart
        # ✅ we create a new cart product 
        new_cart_item = CartProduct(product=product)
        # ✅ We give it the quantity passed through the url
        if qty is not None:         
            new_cart_item.quantity = qty  
        # ✅ we add the new_cart_item to the user's cart 
        cart.items.append(new_cart_item)
        db.session.commit()
        return jsonify(message="cart item added")

    if request.method == "DELETE":
        for cart_item in cart.items:
            if cart_item.product_id == item_id:
                cart.items.remove(cart_item)
                db.session.commit()
                return jsonify(message="cart item deleted")
        return jsonify(message="invalid cart item id") 
        

 