import json
import sqlalchemy as sa
from ...database import db
from ...database.models import User, Notification, NotificationStatus
from .utils import _format_sse
from .helpers import push_to_all, push_to_user, event_stream, _lock, _user_streams


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
        User.id,
        sa.literal("product.published"),
        sa.literal(payload, type_=sa.JSON),        
        sa.literal(NotificationStatus.unread.value),
    )

    stmt = sa.insert(Notification.__table__).from_select(
        ["user_id", "type", "payload", "status"],
        sel,
    )

    db.session.execute(stmt)
    db.session.commit()
