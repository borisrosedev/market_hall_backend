import json
import sqlalchemy as sa
from ..database import db
from ..database.models import User, Notification, NotificationStatus
from .sse import _format_sse
from .stream import _user_streams, _lock


# Helpers d’envoi
def push_to_user(user_id: int, event: str, data: dict) -> None:
    msg = _format_sse(event, data)
    with _lock:
        for q in _user_streams.get(user_id, ()):
            q.put(msg)

def push_to_all(event: str, data: dict) -> None:
    msg = _format_sse(event, data)
    with _lock:
        for queues in _user_streams.values():
            for q in queues:
                q.put(msg)



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
