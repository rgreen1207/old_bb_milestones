import os

from fastapi import APIRouter, Depends
from app.utilities.auth import get_token, UnAuthedMessage
from starlette import status
from .v1 import v1router
from .v1.users.auth.auth_routers import router as auth_router
from .v1.admin.admin_router import router as admin_router
from .v1.cron.cron_router import router as cron_router


ENV: str = os.environ.get("ENV", "local")
JWT_ENFORCED: str = os.environ.get("JWT_ENFORCED", 'False').lower()

if JWT_ENFORCED == "false":
    routers = APIRouter()
else:
    routers = APIRouter(
            dependencies=[Depends(get_token)],
            responses={status.HTTP_401_UNAUTHORIZED: dict(model=UnAuthedMessage)}
        )


auth_routers = APIRouter()
cron_routers = APIRouter()

if JWT_ENFORCED == "false":
    admin_routers = APIRouter()
else:
    admin_routers = APIRouter(
        dependencies=[Depends(get_token)],
        responses={status.HTTP_401_UNAUTHORIZED: dict(model=UnAuthedMessage)}
    )


routers.include_router(v1router)
auth_routers.include_router(auth_router)
admin_routers.include_router(admin_router)
cron_routers.include_router(cron_router)
