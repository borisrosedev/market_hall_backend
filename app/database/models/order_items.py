import enum 
from datetime import datetime
from sqlalchemy import String, Enum, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from .. import db
 
class OrderItems(db.Model): 
    __tablename__ = "order_items"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True) 
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"),
        unique=False,          
        index=True,
        nullable=False,
        ) 
 
    def to_dict(self) -> dict:
        return {
            "id": self.id ,
            "order_id": self.order_id,
             
            }
       
    def __repr__(self) -> str:
        return f"<OrderItems id={self.id} order_id={self.order_id} >"  
