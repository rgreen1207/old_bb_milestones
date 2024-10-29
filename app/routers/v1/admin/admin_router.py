from typing import Annotated

from fastapi import APIRouter, Response, Depends
from app.utilities.auth.auth_handler import AdminSwap, swap_client_uuid_in_jwt, Permissions
from app.actions.clients.user import ClientUserActions
from app.models.admin import AdminCreate, AdminClientSwap

router = APIRouter(tags=["Admin"])


@router.post("/admin/user", response_model_by_alias=True)
async def create_system_admin(
    client_uuid_jwt: Annotated[str, Depends(Permissions(level="2"))],
    new_admin: AdminCreate
):
    client_user = await ClientUserActions.create_client_user(
        data = new_admin.dict(),
        path_params = {"client_uuid": None},
        expand = True
    )
    return client_user


# These two endpoints below cant have endpoint level permission checks since they may be accessed by someone who doesnt
# have a client uuid in their jwt yet (system admin about to select a client to work on.)

# client_uuid_list will not part of v1.0, but may be added in future iteration
# @router.get("/admin", response_model_by_alias=True)
# async def get_possible_clients(
#   decoded_jwt: Annotated[dict, Depends(AdminSwap())]
# ):
#   return decoded_jwt['client_uuid_list']


@router.post("/admin/{client_uuid}", response_model_by_alias=True)
async def swap_client_uuid(
    decoded_jwt: Annotated[dict, Depends(AdminSwap())],
    client_uuid: str,
    response: Response
):
    old_client_uuid = decoded_jwt["client_uuid"]
    new_jwt = await swap_client_uuid_in_jwt(decoded_jwt, client_uuid)

    await ClientUserActions.update_admin_client_user(
        {"client_uuid": old_client_uuid, "user_uuid": decoded_jwt["uuid"]},
        AdminClientSwap(client_uuid=client_uuid)
    )

    response.headers["Bearer"] = new_jwt
    return True
