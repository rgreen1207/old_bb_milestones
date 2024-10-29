from typing import Annotated

from fastapi import APIRouter, Depends
from app.routers.v1.pagination import Page
from app.routers.v1.dependencies import default_query_params, test_mode
from app.actions.users import UserActions
from app.models.base_class import DeleteWarning
from app.models.users import UserUpdate, UserCreate, UserExpanded, UserResponse, UserDelete
from app.utilities.auth.auth_handler import Permissions


router = APIRouter(tags=["Users"])


@router.get("/users", response_model=Page[UserResponse])
async def get_users(
    client_uuid: Annotated[str, Depends(Permissions(level="2"))],
    query_params: dict = Depends(default_query_params)
):
    return await UserActions.get_all_users(query_params)


@router.get("/users/{user_uuid}", response_model=UserExpanded)
async def get_user(
        client_uuid: Annotated[str, Depends(Permissions(level="1"))],
        user_uuid: str,
        expand_services: bool = False
):
    return await UserActions.get_user(user_uuid, expand_services)


@router.post("/users", response_model=UserExpanded)
async def create_user(
        client_uuid: Annotated[str, Depends(Permissions(level="1"))],
        users: UserCreate,
        expand_services: bool = False
):
    return await UserActions.create_user(users, expand_services)


@router.put("/users/{user_uuid}", response_model=UserResponse)
async def update_user(
        client_uuid: Annotated[str, Depends(Permissions(level="1"))],
        user_uuid: str, users_updates: UserUpdate
):
    return await UserActions.update_user(user_uuid, users_updates)


@router.delete("/users/{user_uuid}", response_model=UserDelete|DeleteWarning)
async def delete_user(
        client_uuid: Annotated[str, Depends(Permissions(level="2"))],
        user_uuid: str):
    return await UserActions.delete_user(user_uuid)



@router.delete("/delete_test_user/{user_uuid}", dependencies=[Depends(test_mode)])
async def delete_test_user(
        client_uuid: Annotated[str, Depends(Permissions(level="2"))],
        user_uuid: str
):
    from fastapi import Response
    await UserActions.delete_test_user(user_uuid)
    return Response(status_code=200, content="Test User Deleted")
