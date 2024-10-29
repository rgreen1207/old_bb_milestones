import os
from typing import Annotated

from fastapi import APIRouter, Depends
from app.models.uploads import UploadFile, UploadType

from app.actions.clients.upload import ClientUploadActions
from app.utilities.auth.auth_handler import Permissions, check_jwt_client_with_client

test_mode = os.getenv("TEST_MODE", False)

router = APIRouter(tags=["Upload"], prefix="/clients/{client_uuid}")


@router.get("/upload", response_model_by_alias=True)
async def get_upload_url(
        client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
        client_uuid: str,
        file_name: str,
        upload_type: UploadType):
    await check_jwt_client_with_client(client_uuid_jwt, client_uuid)
    return await ClientUploadActions.get_upload_url(upload_type.value, file_name, client_uuid)


@router.post("/upload", response_model_by_alias=True)
async def post_upload_url(
        client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
        client_uuid: str,
        file_name: UploadFile):
    await check_jwt_client_with_client(client_uuid_jwt, client_uuid)
    return await ClientUploadActions.process_roster_file(file_name, client_uuid)
