from fastapi import APIRouter

from app.api.routes import api_v1_auth, api_v1_files, api_v1_products, api_v1_users
from app.core.config import settings

api_router = APIRouter()
api_router.include_router(api_v1_auth)
api_router.include_router(api_v1_users)
api_router.include_router(api_v1_files)
api_router.include_router(api_v1_products)


# if settings.ENVIRONMENT == "local":
#     api_router.include_router(private.router)
