from uuid import UUID
from typing import Any, Union
from sqlmodel import Session, select, delete
from app.utils import save_file
from app.api.deps import _coerce_obj_id, create_unique_filename
from app.core.security import get_password_hash, verify_password
from app.models.db_models.product import Product
from app.models.non_db_models.product import ProductDTO, ProductCreateRequest
from fastapi import UploadFile

def get_all_products(*, session: Session) -> list[ProductDTO] | None:
    statement = select(Product).order_by(Product.created_at.desc())
    return list(session.exec(statement=statement).all())

def get_one_product_by_id(*, session: Session, id: Union[int | UUID | str]) -> ProductDTO | None:
    coerced_id = _coerce_obj_id(id)
    statement = select(Product).where(Product.id == coerced_id)
    selected_product = session.exec(statement).first()
    return selected_product

def create_one_product(*, session: Session, uploaded_file: UploadFile, product_create: ProductCreateRequest) -> ProductDTO:  
    unique_filename = create_unique_filename(uploaded_file.filename)
    save_file(file=uploaded_file,need_unique_name=False,unique_name=unique_filename, uploaded_file_specific_folder="products")
    db_obj = Product.model_validate(
        product_create,
        update={"photo_name": unique_filename}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj

def delete_one_product_by_id(*, session: Session, id: Union[int | UUID | str]):
    coerced_id = _coerce_obj_id(id)
    statement = delete(Product).where(Product.id == coerced_id)
    delete_response = session.exec(statement)
    return delete_response