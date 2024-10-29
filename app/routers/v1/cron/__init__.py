from .cron_router import router as cron_router
from fastapi import APIRouter

v1_cron_router = APIRouter()
v1_cron_router.include_router(cron_router)