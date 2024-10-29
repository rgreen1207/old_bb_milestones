from typing import Annotated

from fastapi import APIRouter, Depends
from app.routers.v1.dependencies import default_query_params, verify_program_award
from app.routers.v1.pagination import Page
from app.actions.programs.awards.program_award_actions import ProgramAwardActions
from app.models.uploads import UploadType
from app.models.base_class import DeleteWarning
from app.models.programs import ProgramAwardCreate, ProgramAwardUpdate, ProgramAwardResponse, ProgramAwardDelete
from app.utilities.auth.auth_handler import Permissions, check_jwt_client_with_client


router = APIRouter(
    prefix="/clients/{client_uuid}/programs/{program_9char}",
    tags=["Client Program Awards"]
)


def path_params(
    client_uuid: str,
    program_9char: str,
    client_award_9char: str=None,
    program_award_9char: str=None
):
    return {
        "client_uuid": client_uuid,
        "program_9char": program_9char,
        "client_award_9char": client_award_9char,
        "program_award_9char": program_award_9char
    }


@router.get("/awards", response_model=Page[ProgramAwardResponse])
async def get_awards(
    client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
    path_params: dict = Depends(path_params),
    query_params: dict = Depends(default_query_params)
):
    await check_jwt_client_with_client(client_uuid_jwt, path_params["client_uuid"])
    return await ProgramAwardActions.get_program_awards(path_params, query_params)


@router.get("/awards/{program_award_9char}", response_model=ProgramAwardResponse)
async def get_award(
    client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
    path_params: dict = Depends(path_params)
):
    await check_jwt_client_with_client(client_uuid_jwt, path_params["client_uuid"])
    return await ProgramAwardActions.get_award(path_params)


@router.get(
        "/awards/{program_award_9char}/upload",
        dependencies=[Depends(verify_program_award)]
    )
async def get_program_award_upload_url(
    file_name: str,
    upload_type: UploadType,
    path_params: dict = Depends(path_params)
):
    return await ProgramAwardActions.get_upload_url(path_params, file_name, upload_type.value)


@router.post("/awards/{client_award_9char}", response_model=list[ProgramAwardResponse] | ProgramAwardResponse)
async def create_award(
    client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
    awards: list[ProgramAwardCreate] | ProgramAwardCreate,
    path_params: dict = Depends(path_params),
):
    await check_jwt_client_with_client(client_uuid_jwt, path_params["client_uuid"])
    return await ProgramAwardActions.create_award(path_params, awards)


@router.put("/awards/{program_award_9char}", response_model=ProgramAwardResponse)
async def update_award(
    client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
    award_updates: ProgramAwardUpdate,
    path_params: dict = Depends(path_params)
):
    await check_jwt_client_with_client(client_uuid_jwt, path_params["client_uuid"])
    return await ProgramAwardActions.update_award(path_params, award_updates)


@router.delete("/awards/{program_award_9char}", response_model=ProgramAwardDelete|DeleteWarning)
async def delete_award(
    client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
    path_params: dict = Depends(path_params)
):
    await check_jwt_client_with_client(client_uuid_jwt, path_params["client_uuid"])
    return await ProgramAwardActions.delete_award(path_params)
