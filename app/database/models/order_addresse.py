import enum 
from datetime import datetime
from sqlalchemy import String, Enum, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from .. import db

class TypeOrderAddresses(enum.Enum):
    shipping = "shipping"
    billing = "billing"
    
class OrderAddresse(db.Model): 
    __tablename__ = "order_addresses"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True) 
    order_id: Mapped[int] = mapped_column(
        ForeignKey("order.id", ondelete="CASCADE"),
        unique=False,          
        index=True,
        nullable=False,
        ) 
   
    type: Mapped[TypeOrderAddresses] = mapped_column(Enum(TypeOrderAddresses) )
    full_name: Mapped[str] = mapped_column( nullable=False)
    line1 : Mapped[str] = mapped_column (  nullable=False)  
    line2 : Mapped[str] = mapped_column (  nullable=True)
    city : Mapped[str] = mapped_column (  nullable=False) 
    postal_code : Mapped[str] = mapped_column ( nullable=False)
    country : Mapped[str] = mapped_column (  nullable=False)
    phone: Mapped[str] = mapped_column ( nullable=True)
    def to_dict(self) -> dict:
        return {
            "id": self.id ,
            "order_id": self.order_id,
            "type" : self.type.value, 
            "full_name" : self.full_name, 
            "line1":self.line1,
            "line2":self.line2,
            "city": self.city, 
            "postal_code":self.postal_code,
            "country":self.country,
            "phone":self.phone,
            }
       
    def __repr__(self) -> str:
        return f"<OrderAddresse id={self.id} order_id={self.order_id} type{self.type!r} full_name={self.full_name} line1={self.line1} line2={self.line2} \
            city={self.city} postal_code={self.postal_code} country={self.country} phone={self.phone}  >"  
