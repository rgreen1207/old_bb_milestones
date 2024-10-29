from .awards_router import router as awards_router
from fastapi import APIRouter

v1_awards_router = APIRouter()
v1_awards_router.include_router(awards_router)
