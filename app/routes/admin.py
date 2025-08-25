from flask import Blueprint, jsonify, request
from ..services import admin_required, notify_all_users_product_published
from ..database import db
from ..database.models import Product, User
from ..services import push_to_all
from ..utils import to_bool
import re

api_v1_admin=Blueprint("api_v1_admin", __name__, url_prefix="/api/v1/admins")

EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"

@api_v1_admin.route("/users/<int:user_id>/update", methods=["GET"])
@admin_required
def update_user_profile(user_id):
    args=request.args
    if not args:
        return jsonify(message=f"invalid update request, no arguments"), 404
    user = db.session.execute(db.select(User).filter_by(id=user_id)).scalar_one_or_none()
    if not user:
        return jsonify(message=f"user with id {user_id} not found"), 404
    if args.get('banned'):
        val = to_bool(args.get('banned'))
        if val is not  None:
            user.is_banned = val
    if args.get('email'):
        val = args.get('email')
        if not re.match(EMAIL_REGEX, val):
            return jsonify(message="user not updated, invalid email"), 400
    if args.get('password'):
        val = args.get('passord')
        user.password = val
    db.session.commit()
    return jsonify(message=f"user {user_id} updated")


@api_v1_admin.route("/products/<int:product_id>/publish", methods=["POST"])
@admin_required
def publish_product(product_id):
    """ publish a product and sse-notify it and db-batch-notify-it """
    product = db.session.get(Product, product_id)
    if not product:
        return jsonify(message="product not found"), 404

    product.status = "published"

    db.session.commit()

    # batch notification
    notify_all_users_product_published(product)
    push_to_all(
        "notification.created",
        {"p_id": product.id, "p_name": product.name, "p_photo_name": product.photo_name},
    )
    return jsonify(message=f"product with id: {product.id} published and notifications sent")