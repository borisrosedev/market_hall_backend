from sqlalchemy.orm import Session
from sqlalchemy import event
from ..models import CartProduct

@event.listens_for(Session, "before_flush")
def delete_zero_qty_items(session, flush_context, instances):
    """ Deletes Zero Quantity Items """
    for obj in list(session.dirty):
        if isinstance(obj, CartProduct) and obj.quantity is not None and obj.quantity <= 0:
            session.delete(obj)

    for obj in list(session.new):
        if isinstance(obj, CartProduct) and obj.quantity is not None and obj.quantity <= 0:
            session.expunge(obj)
