from fastapi import APIRouter, Depends
from typing import Union, Annotated
from app.routers.v1.pagination import Page
from app.models.messages import MessageCreate, MessageUpdate, MessageSend, MessageResponse
from app.actions.messages.message_actions import MessageActions
from app.routers.v1.dependencies import default_query_params
from app.utilities.auth.auth_handler import Permissions
from app.routers.v1.messages.message_router import MessageEventRouter

router = APIRouter(
    prefix="/clients/{client_uuid}/programs/{program_9char}",
    tags=["Program Messages"],
    route_class=MessageEventRouter
)


def path_params(client_uuid: str, program_9char: str):
    return {
        "client_uuid": client_uuid,
        "program_9char": program_9char
    }


@router.get("/messages", response_model=Page[MessageResponse])
async def get_program_messages(
    client_uuid: Annotated[str, Depends(Permissions(level="2"))],
    path_params: dict = Depends(path_params),
    query_params: dict = Depends(default_query_params)
):
    return await MessageActions.get_all_program_messages(query_params, path_params)


@router.get("/messages/{message_9char}", response_model=MessageResponse)
async def get_program_message(
    client_uuid: Annotated[str, Depends(Permissions(level="2"))],
    message_9char: str,
    path_params: dict = Depends(path_params),
):
    return await MessageActions.get_program_message(message_9char, path_params)


@router.post("/messages", response_model=list[MessageResponse] | MessageResponse)
async def create_program_message(
    client_uuid: Annotated[str, Depends(Permissions(level="2"))],
    new_message_obj: Union[list[MessageCreate], MessageCreate],
    path_params: dict = Depends(path_params),
):
    return await MessageActions.create_message(new_message_obj, path_params)


@router.put("/messages/{message_9char}", response_model=MessageResponse)
async def update_message(
    client_uuid: Annotated[str, Depends(Permissions(level="2"))],
    message_9char: str,
    message_updates: MessageUpdate
):
    return await MessageActions.update_message(message_9char, message_updates)


@router.post("/messages/{message_9char}/send")
async def send_message(
    client_uuid: Annotated[str, Depends(Permissions(level="2"))],
    message_9char: str,
    send_model: MessageSend
):
    return await MessageActions.send_message(message_9char, send_model)
