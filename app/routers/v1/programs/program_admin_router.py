from typing import Union, Annotated
from fastapi import APIRouter, Query, Depends
from app.routers.v1.dependencies import default_query_params
from app.routers.v1.pagination import Page
from app.models.base_class import DeleteWarning
from app.models.programs import AdminUpdate, AdminCreate, AdminStatus, AdminModel, AdminDelete
from app.actions.programs.admins import ProgramAdminActions
from app.utilities.auth.auth_handler import Permissions, check_jwt_client_with_client

router = APIRouter(prefix="/clients/{client_uuid}/programs/{program_9char}", tags=["Client Program Admins"])


def path_params(client_uuid: str, program_9char: str, user_uuid: str= None):
    return {"client_uuid": client_uuid, "program_9char": program_9char, "user_uuid": user_uuid}

def query_params(offset: int, limit: int = Query(default=100, lte=100)):
    return {"offset": offset, "limit": limit}


@router.get("/admins", response_model=Page[AdminModel])
async def get_admins(
    client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
    query_params: dict = Depends(default_query_params),
    path_params: dict = Depends(path_params)
):
    await check_jwt_client_with_client(client_uuid_jwt, path_params["client_uuid"])
    return await ProgramAdminActions.get_program_admins(path_params, query_params)


@router.get("/admins/{user_uuid}", response_model=AdminModel)
async def get_admin(
    client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
    path_params: dict = Depends(path_params)
):
    await check_jwt_client_with_client(client_uuid_jwt, path_params["client_uuid"])
    return await ProgramAdminActions.get_program_admin(path_params)


@router.post("/admins", response_model= Union[list[AdminStatus], AdminStatus])
async def create_admin(
    client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
    path_params: dict = Depends(path_params),
    admins: Union[AdminCreate, list[AdminCreate]] = Depends(ProgramAdminActions.check_existing)
):
    await check_jwt_client_with_client(client_uuid_jwt, path_params["client_uuid"])
    return await ProgramAdminActions.create_program_admins(path_params, admins)


@router.put("/admins/{user_uuid}", response_model=AdminModel)
async def update_admin(
    client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
    admin_updates: AdminUpdate,
    path_params: dict = Depends(path_params)
):
    await check_jwt_client_with_client(client_uuid_jwt, path_params["client_uuid"])
    return await ProgramAdminActions.update_program_admin(path_params, admin_updates)


@router.delete("/admins/{user_uuid}", response_model=AdminDelete|DeleteWarning)
async def delete_admin(
    client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
    path_params: dict = Depends(path_params)
):
    await check_jwt_client_with_client(client_uuid_jwt, path_params["client_uuid"])
    return await ProgramAdminActions.delete_program_admin(path_params)
