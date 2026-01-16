from sqlalchemy.orm import Session
from sqlalchemy import event
from ...models.db_models import __all_db_models__ as models


@event.listens_for(Session, "before_flush")
def delete_zero_qty_items(session, flush_context, instances):
    """Deletes Zero Quantity Items"""
    for obj in list(session.dirty):
        if isinstance(obj, models.CartProduct) and obj.quantity is not None and obj.quantity <= 0:
            session.delete(obj)

    for obj in list(session.new):
        if isinstance(obj, models.CartProduct) and obj.quantity is not None and obj.quantity <= 0:
            session.expunge(obj)
