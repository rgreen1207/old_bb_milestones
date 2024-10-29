from typing import Annotated

from fastapi import APIRouter, Depends
from app.routers.v1.dependencies import default_query_params
from app.models.users import UserServiceUpdate, UserServiceCreate, ServiceDelete, ServiceStatus, ServiceBulk, UserServiceResponse, ServiceListResponse
from app.actions.users.services import UserServiceActions
from app.utilities.auth.auth_handler import Permissions

router = APIRouter(tags=["Users Service"], prefix="/users/{user_uuid}")

@router.get("/services", response_model=ServiceListResponse)
async def get_services(
    client_uuid: Annotated[str, Depends(Permissions(level="1"))],
    user_uuid: str,
    query_params: dict = Depends(default_query_params)
):
    return await UserServiceActions.get_all_services(user_uuid, query_params)


@router.get("/services/{service_uuid}", response_model=UserServiceResponse)
async def get_service(
        client_uuid: Annotated[str, Depends(Permissions(level="1"))],
        user_uuid: str, service_uuid: str
):
    return await UserServiceActions.get_service(user_uuid, service_uuid)


@router.post("/services", response_model=ServiceStatus)
async def create_service(
    client_uuid: Annotated[str, Depends(Permissions(level="1"))],
    user_uuid: str,
    user_service: UserServiceCreate = Depends(UserServiceActions.check_existing)
):
    return await UserServiceActions.create_user_service(user_uuid, user_service)


@router.put("/services/{service_uuid}", response_model=UserServiceResponse)
async def update_service(
    client_uuid: Annotated[str, Depends(Permissions(level="1"))],
    user_uuid: str,
    service_uuid: str,
    service_updates: UserServiceUpdate
):
    return await UserServiceActions.update_service(user_uuid, service_uuid, service_updates)


@router.put("/services", response_model=list[UserServiceResponse])
async def bulk_update_services(
        client_uuid: Annotated[str, Depends(Permissions(level="1"))],
        user_uuid: str, updates: list[ServiceBulk]
):
    return await UserServiceActions.bulk_update_services(user_uuid, updates)


@router.delete("/services/{service_uuid}")
async def delete_service(
        client_uuid: Annotated[str, Depends(Permissions(level="1"))],
        service_uuid: str
):
    return await UserServiceActions.delete_service(service_uuid)


@router.delete("/services")
async def bulk_delete_service(
        client_uuid: Annotated[str, Depends(Permissions(level="2"))],
        service_delete: list[ServiceDelete]
):
    return await UserServiceActions.bulk_delete_services(service_delete)
