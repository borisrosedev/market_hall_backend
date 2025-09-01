import enum 
from datetime import datetime
from typing import Any, Dict, Optional
from sqlalchemy import String,  ForeignKey, Index, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import JSON
from .. import db
 
class OrderItem(db.Model): 
    __tablename__ = "order_items"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True) 
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"), 
        unique=False,          
        index=True,
        nullable=False,
        ) 
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"), 
        unique=False,          
        index=True,
        nullable=False,
    )
    #order: Mapped["Order"] = relationship(back_populates="order_products")
    #product: Mapped["Product"] = relationship(back_populates="order_products")
    sku:Mapped[str] = mapped_column(nullable=False) 
    product_name:Mapped[str] = mapped_column(nullable=False) 
    unit_price_cents: Mapped[int] = mapped_column(nullable=False,default=1) # -- fixed unit prise
    quantity: Mapped[int] = mapped_column(nullable=False,default=1)  
    subtotal_cents: Mapped[int] = mapped_column(nullable=False )   # -- unit_price_cents * quantity (avant taxes/remises ligne)
    tax_cents: Mapped[int] = mapped_column(nullable=False,default=0)   
    discount_cents: Mapped[int] = mapped_column(nullable=False,default=0) 
    total_cents: Mapped[int] = mapped_column(nullable=False,default=0)
    currency: Mapped[str] = mapped_column(String(3),default='EUR', nullable=False) 
    #variant_json  # JSONB, -- ex. color, size
    variant_json: Mapped[Optional[Dict[str, Any]]] = mapped_column(
        JSON,
        nullable=True,
    )
    #metadata_json # JSONB, -- free (ex: used for strip item ref )   
    metadata_json: Mapped[Optional[Dict[str, Any]]] = mapped_column(
        JSON,
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
     

    def to_dict(self) -> dict:
        return {
            "id": self.id ,
            "order_id": self.order_id,
            "product_id": self.product_id, 
            "sku": self.sku, 
            "product_name": self.product_name, 
            "unit_price_cents": self.unit_price_cents, 
            "quantity": self.quantity,             
            "subtotal_cents": self.subtotal_cents, 
            "tax_cents": self.tax_cents,             
            "discount_cents": self.discount_cents, 
            "total_cents": self.total_cents,             
            "currency": self.currency, 
            "variant_json": self.variant_json,  
            "metadata_json": self.metadata_json,  
            "created_at": self.created_at,  
            }
       
    def __repr__(self) -> str:
        return f"<OrderItem id={self.id} order_id={self.order_id} product_id={self.product_id} \
            sku={self.sku}  product_name={self.product_name}  unit_price_cents={self.unit_price_cents}  quantity={self.quantity}  subtotal_cents={self.subtotal_cents}  itax_cents={self.tax_cents} \
            discount_cents={self.discount_cents}  total_cents={self.total_cents}  currency={self.currency}  variant_json={self.variant_json}  metadata_json={self.metadata_json}  created_at={self.created_at}  >"  
