from fastapi import APIRouter
from .user_router import router as users_router
from .user_service_router import router as user_service_router


v1_users_router = APIRouter()
v1_users_router.include_router(users_router)
v1_users_router.include_router(user_service_router)

