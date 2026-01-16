from flask import Blueprint, jsonify, session, request
from ..services.decorators import __all_decorators__
from ...database import db
from ...models.db_models.user import User
from ...models.db_models.cart import Cart
from ...models.db_models.product import Product
from ...models.db_models.cart_product import CartProduct
from ..utils.type_utils import to_int
from ..services.decorators.auth import session_required, admin_required


api_v1_carts = Blueprint("api_v1_cart", __name__, url_prefix="/api/v1/carts")


@api_v1_carts.route("/", methods=["GET"])
@admin_required
def get_all_carts():
    carts = db.session.execute(db.select(Cart).order_by(Cart.id)).scalars()
    return jsonify(carts=[cart.to_dict() for cart in carts])


@api_v1_carts.route("/me", methods=["GET"])
@session_required
def get_current_user_cart():
    """Get the current user cart"""
    cart = db.session.execute(db.select(Cart).filter_by(user_id=session["user_id"])).scalar()
    if not cart:
        return jsonify(message="invalid data"), 400
    return jsonify(cart=cart.to_dict())


@api_v1_carts.route("/<int:cart_id>/items", methods=["DELETE"])
@session_required
def delete_all_items_from_cart(cart_id):
    user = db.session.execute(
        db.select(User).filter_by(email=session["email"])
    ).scalar_one_or_none()
    if not user:
        return jsonify(message="invalid data"), 400

    cart = db.session.execute(db.select(Cart).filter_by(id=user.cart.id)).scalar_one_or_none()
    if not cart:
        return jsonify(message="invalid cart id"), 400

    cart.items.clear()
    db.session.commit()
    return jsonify(message="all items deleted from cart")


@api_v1_carts.route("/<int:cart_id>/items/<int:item_id>", methods=["GET", "DELETE"])
@session_required
def add_cart_item_or_update_quantity(cart_id, item_id):
    args = request.args

    user = db.session.execute(
        db.select(User).filter_by(email=session["email"])
    ).scalar_one_or_none()
    if not user:
        return jsonify(message="invalid data"), 400

    cart = db.session.execute(db.select(Cart).filter_by(id=user.cart.id)).scalar_one_or_none()
    if not cart:
        return jsonify(message="invalid cart id"), 400

    product = db.session.execute(db.select(Product).filter_by(id=item_id)).scalar_one_or_none()
    if not product:
        return jsonify(message="invalid product id")

    if request.method == "GET":
        qty = to_int(args.get("quantity"), default=1)

        for cart_item in cart.items:
            if cart_item.product_id == item_id:
                if qty is not None:
                    result = cart_item.quantity + qty
                    if result <= 0 or qty == 0:
                        cart.items.remove(cart_item)
                    else:
                        cart_item.quantity = cart_item.quantity + qty
                    db.session.commit()
                    return jsonify(message="cart item quantity updated")

        new_cart_item = CartProduct(product=product)

        if qty is not None and qty > 0:
            new_cart_item.quantity = qty
        else:
            return jsonify(message="invalid cart item quantity"), 400
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
