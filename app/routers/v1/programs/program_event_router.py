from typing import Annotated, Callable
from fastapi import APIRouter, Depends
from app.routers.v1.dependencies import default_query_params, test_mode
from app.routers.v1.pagination import Page
from app.models.programs import ProgramEventModelDB, ProgramEventUpdate, ProgramEventReturn
from app.actions.programs.events.program_event_actions import ProgramEventActions
from app.utilities.auth.auth_handler import Permissions, check_jwt_client_with_client
from fastapi.routing import APIRoute


class ProgramEventRouter(APIRoute):

    event_type: int

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request):
            response = await original_route_handler(request)
            if response.status_code == 200 and request.method in ['POST', 'PUT', 'DELETE']:
                await ProgramEventActions.create_event_from_route(self, request, response)
            return response

        return custom_route_handler


router = APIRouter(
    prefix="/clients/{client_uuid}/programs/{program_9char}",
    tags=["Client Program Events"]
)

def path_params(client_uuid: str, program_9char: str, event_9char: str=None):
    return {
        "client_uuid": client_uuid,
        "program_9char": program_9char,
        "event_9char": event_9char
    }


@router.get("/events", response_model=Page[ProgramEventReturn])
async def get_events(
    client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
    path_params: dict = Depends(path_params),
    query_params: dict = Depends(default_query_params)
):
    await check_jwt_client_with_client(client_uuid_jwt, path_params["client_uuid"])
    return await ProgramEventActions.get_all_program_events(path_params, query_params)


@router.get("/events/{event_9char}", response_model=ProgramEventModelDB)
async def get_event(
    client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
    path_params: dict = Depends(path_params)
):
    await check_jwt_client_with_client(client_uuid_jwt, path_params["client_uuid"])
    return await ProgramEventActions.get_event(path_params)


# @router.post("/events", response_model=(list[ProgramEventModelDB] | ProgramEventModelDB))
# async def create_event(
#     client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
#     events: (list[ProgramEventCreate] | ProgramEventCreate),
#     path_params: dict = Depends(path_params),
#     program_uuid: str = Depends(ProgramEventActions.get_program_uuid)
# ):
#     await check_jwt_client_with_client(client_uuid_jwt, path_params["client_uuid"])
#     return await ProgramEventActions.create_event(events, path_params, program_uuid)


@router.put("/events/{event_9char}", response_model=ProgramEventModelDB)
async def update_event(
    client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
    event_updates: ProgramEventUpdate,
    path_params: dict = Depends(path_params)
):
    await check_jwt_client_with_client(client_uuid_jwt, path_params["client_uuid"])
    return await ProgramEventActions.update_event(event_updates, path_params)


# #TODO: Check, delete is not in endpoint specs doc
# @router.delete("/events/{event_9char}")
# async def delete_event(
#     client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
#     path_params: dict = Depends(path_params)
# ):
#     await check_jwt_client_with_client(client_uuid_jwt, path_params["client_uuid"])
#     return await ProgramEventActions.delete_event(path_params)

# this route is only available when running application locally or with pytests
@router.delete("/delete_program_events/{event_9char}", dependencies=[Depends(test_mode)])
async def delete_event(
    client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
    path_params: dict = Depends(path_params)
):
    from fastapi import Response
    await ProgramEventActions.delete_event(path_params)
    return Response(status_code=200, content="Test Program Event Deleted")
