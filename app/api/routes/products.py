from typing import Optional, Annotated, Literal, Union, Any
from enum import StrEnum
from pydantic import BaseModel, Field
from datetime import datetime, timezone
import re, shutil, uuid, logging
import os
from pathlib import Path as P
from fastapi import FastAPI, Body, Query, Path, Cookie, Response, status, File, UploadFile, Form, HTTPException, Depends
from fastapi import APIRouter
from app.core.config import settings
from app.models.non_db_models.product import ProductDTOResponse, ProductCreateRequest
from app.models.non_db_models.message import Message

from app.api.deps import (
    CookieCurrentUser,
    SessionDep,
    get_current_active_superuser,
)
from app.utils import generate_new_account_email, send_email
from app.api.crud.products import get_all_products, get_one_product_by_id, delete_one_product_by_id, create_one_product


# ----------- CONFIG AND DEBUG -------------
BASE_DIR = P(__file__).resolve().parent.parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)
logging.basicConfig(level=logging.DEBUG)
# ----------- END OF CONFIG AND DEBUG -------------

api_v1_products = APIRouter(
    prefix="/products",
    tags=["products"]
)


@api_v1_products.get("/{product_id}")
async def read_one_produc(product_id:uuid.UUID, session:SessionDep):
    product = get_one_product_by_id(id=product_id,session=session)
    if not product:
        raise HTTPException(
            status_code=404,
            detail="no product found",
        )
    return { "product": product}

@api_v1_products.post("/")
async def create_product(
    session: SessionDep,
    name: str = Form(...),
    description: str = Form(...),
    price_cents: int = Form(...),
    sku: str = Form(...),
    quantity: int = Form(...),
    file: Optional[UploadFile] = File(None)
):
    logging.debug(f"✅ name: {name}, price: {price_cents}, qty: {quantity}, description: {description}")

    if not file:
        raise HTTPException(
            status_code=400,
            detail="error adding product: no file",
        )

    product_in = {
        "name": name,
        "price_cents": price_cents,
        "sku": sku,
        "quantity": quantity,
        "description": description
    }

    new_product = create_one_product(session=session, product_create=product_in, uploaded_file=file)
    if not new_product:
        raise HTTPException(
            status_code=400,
            detail="error adding product",
        )
    return {"message": "product created"}