from app.routers.v1.admin.admin_router import router as admin_router
from fastapi import APIRouter

v1_admin_router = APIRouter()
v1_admin_router.include_router(admin_router)
