from fastapi import APIRouter
from .awards import v1_awards_router
from .clients import v1_clients_router
from .programs import v1_program_router
from .messages import v1_messages_router
from .segments import v1_segments_router
from .users import v1_users_router
from .client_upload import v1_upload_router

v1router = APIRouter()
v1router.include_router(v1_awards_router)
v1router.include_router(v1_users_router)
v1router.include_router(v1_clients_router)
v1router.include_router(v1_program_router)
v1router.include_router(v1_messages_router)
v1router.include_router(v1_segments_router)
v1router.include_router(v1_upload_router)

@v1router.get("/health", status_code=418)
async def read_root():
    return {"message": "milestones is up and brewing tea"}
