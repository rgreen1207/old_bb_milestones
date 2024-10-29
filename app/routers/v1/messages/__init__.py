from .message_router import router as message_routes
from fastapi import APIRouter

v1_messages_router = APIRouter()

v1_messages_router.include_router(message_routes)
