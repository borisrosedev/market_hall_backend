from flask import Blueprint, jsonify
from ..services import admin_required, notify_all_users_product_published
from ..database import db
from ..database.models import Product
from ..services import push_to_all

api_v1_admin=Blueprint("api_v1_admin", __name__, url_prefix="/api/v1/admin")

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