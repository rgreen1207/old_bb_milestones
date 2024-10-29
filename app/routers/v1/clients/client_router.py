from typing import Annotated
from fastapi import APIRouter, Depends
from app.actions.programs.events.program_event_actions import ProgramEventActions
from app.models.programs.program_event_models import ProgramEventReturn
from app.routers.v1.pagination import Page
from app.routers.v1.dependencies import default_query_params, test_mode
from app.models.base_class import DeleteWarning
from app.models.clients import ClientUpdate, ClientCreate, ClientResponse, ClientDelete
from app.actions.clients.client_actions import ClientActions
from app.utilities.auth.auth_handler import Permissions, check_jwt_client_with_client

router = APIRouter(tags=["Clients"])


@router.get("/clients", response_model=Page[ClientResponse])
async def get_clients(
    client_uuid: Annotated[str, Depends(Permissions(level="2"))],
    query_params: dict = Depends(default_query_params)
):# -> Page[ClientModel]
    return await ClientActions.get_all_clients(query_params)

@router.get("/clients/{client_uuid}", response_model=ClientResponse)
async def get_client(
        client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
        client_uuid: str
):
    await check_jwt_client_with_client(client_uuid_jwt, client_uuid)
    return await ClientActions.get_client(client_uuid)


@router.post("/clients", response_model=list[ClientResponse]|ClientResponse)
async def create_client(
    client_uuid_jwt: Annotated[str, Depends(Permissions(level="2"))],
    clients: list[ClientCreate] | ClientCreate
):
    return await ClientActions.create_client(clients)


@router.put("/clients/{client_uuid}", response_model=ClientResponse)
async def update_client(
    client_uuid_jwt: Annotated[str, Depends(Permissions(level="2"))],
    client_uuid: str,
    client_updates: ClientUpdate
):
    await check_jwt_client_with_client(client_uuid_jwt, client_uuid)
    return await ClientActions.update_client(client_uuid, client_updates)


# this should only work if there is nothing else associated with the client
@router.delete("/clients/{client_uuid}", response_model=ClientDelete|DeleteWarning)
async def delete_client_by_uuid(
        client_uuid_jwt: Annotated[str, Depends(Permissions(level="2"))],
        client_uuid: str
):
    await check_jwt_client_with_client(client_uuid_jwt, client_uuid)
    #TODO: add check to see if there is anything else associated with the client
    return await ClientActions.delete_client(client_uuid)

@router.get("/clients/{client_uuid}/events", response_model=Page[ProgramEventReturn])
async def get_all_client_events(
    client_uuid_jwt: Annotated[str, Depends(Permissions(level="2"))],
    client_uuid: str,
    query_params: dict = Depends(default_query_params)
):
    return await ProgramEventActions.get_all_client_events(client_uuid, query_params)





# this route can only be accessed through postman/pytests when running locally.
@router.delete("/clients/{client_uuid}/delete_client_events", dependencies=[Depends(test_mode)])
async def delete_all_client_test_events(
    client_uuid_jwt: Annotated[str, Depends(Permissions(level="2"))],
    client_uuid: str,
):
    return await ClientActions.delete_all_client_events(client_uuid)

# this route can only be accessed through postman/pytests when running locally
# in test_mode program_9char is hardcoded in the request to "test_mesg"
@router.delete("/delete_all_message_events", dependencies=[Depends(test_mode)])
async def delete_all_test_messages(
    client_uuid_jwt: Annotated[str, Depends(Permissions(level="2"))],
    program_9char: str = "test_mesg",
):
    return await ClientActions.delete_all_test_message_events(program_9char)
