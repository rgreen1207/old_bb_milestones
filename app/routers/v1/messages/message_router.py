from fastapi import APIRouter, Depends
from fastapi.routing import APIRoute
from typing import Union, Annotated, Callable
from app.actions.programs.events.program_event_actions import ProgramEventActions
from app.routers.v1.pagination import Page
from app.models.base_class import DeleteWarning
from app.models.messages import MessageCreate, MessageUpdate, MessageSend, MessageResponse, MessageDelete
from app.actions.messages.message_actions import MessageActions
from app.routers.v1.dependencies import default_query_params
from app.utilities.auth.auth_handler import Permissions

class MessageEventRouter(APIRoute):
    event_type = 3

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request):
            response = await original_route_handler(request)
            if response.status_code == 200 and request.method in ['POST', 'PUT', 'DELETE']:
                await ProgramEventActions.create_event_from_route(self, request, response)
            return response

        return custom_route_handler


router = APIRouter(tags=["Messages"], route_class=MessageEventRouter)


@router.get("/messages", response_model=Page[MessageResponse])
async def get_messages(
        client_uuid: Annotated[str, Depends(Permissions(level="2"))],
        query_params: dict = Depends(default_query_params)
):
    return await MessageActions.get_all(query_params)


@router.get("/messages/client/{client_uuid}", response_model=Page[MessageResponse])
async def get_client_messages(
    client_uuid: str,
    query_params: dict = Depends(default_query_params)
):
    return await MessageActions.get_all_client_messages(client_uuid, query_params)


@router.get("/messages/{message_9char}", response_model=MessageResponse)
async def get_message(
        client_uuid: Annotated[str, Depends(Permissions(level="2"))],
        message_9char: str
):
    return await MessageActions.get_one(message_9char)


@router.post("/messages", response_model= list[MessageResponse]|MessageResponse)
async def create_message(
        client_uuid: Annotated[str, Depends(Permissions(level="2"))],
        new_message_obj: Union[list[MessageCreate], MessageCreate]
):
    return await MessageActions.create_message(new_message_obj)


# TODO: Role this functionality into create_message
# only difference is the template_uuid being passed in the body
@router.post("/messages/{message_9char}/template", deprecated=True)
async def create_message_from_template(
        client_uuid: Annotated[str, Depends(Permissions(level="2"))],
        message_9char: str
):
    return {"message": f"Created message from template for {message_9char}"}


# send message to program audience
@router.post("/messages/{message_9char}/send")
async def send_message(
        client_uuid: Annotated[str, Depends(Permissions(level="2"))],
        message_9char: str,
        send_model: MessageSend
):
    return await MessageActions.send_message(message_9char, send_model)


@router.put("/messages/{message_9char}", response_model=MessageResponse)
async def update_message(
        client_uuid: Annotated[str, Depends(Permissions(level="2"))],
        message_9char: str, message_updates: MessageUpdate
):
    return await MessageActions.update_message(message_9char, message_updates)


@router.delete("/messages/{message_9char}", response_model=MessageDelete|DeleteWarning)
async def delete_message(
        client_uuid: Annotated[str, Depends(Permissions(level="2"))],
        message_9char: str
):
    return await MessageActions.delete_message(message_9char)
