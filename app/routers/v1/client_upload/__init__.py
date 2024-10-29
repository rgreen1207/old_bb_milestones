from fastapi import APIRouter
from .client_upload_router import router as upload_router


v1_upload_router = APIRouter()
v1_upload_router.include_router(upload_router)
