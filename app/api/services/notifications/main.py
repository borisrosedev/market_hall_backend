import json
import sqlalchemy as sa
from ....database import db
from ....models.db_models import (__all_db_models__ as db_model)



def notify_all_users_product_published(product) -> None:
    """
    Create a notification for all users.
    """
    payload = {
        "p_id": product.id,
        "p_name": product.name,
        "p_photo_name": getattr(product, "photo_name", None)
    }
    sel = sa.select(
        db_model.User.id,
        sa.literal("product.published"),
        sa.literal(payload, type_=sa.JSON),        
        sa.literal(db_model.NotificationStatus.unread.value),
    )

    stmt = sa.insert(db_model.Notification.__table__).from_select(
        ["user_id", "type", "payload", "status"],
        sel,
    )

    db.session.execute(stmt)
    db.session.commit()
