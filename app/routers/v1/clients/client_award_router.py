from typing import Annotated, Callable
from fastapi import APIRouter, Depends
from fastapi.routing import APIRoute
from app.routers.v1.pagination import Page
from app.routers.v1.dependencies import default_query_params, verify_client_award
from app.models.base_class import DeleteWarning
from app.actions.clients.awards.client_award_actions import ClientAwardActions
from app.actions.programs.events.program_event_actions import ProgramEventActions
from app.models.clients import ClientAwardCreate, ClientAwardUpdate, ClientAwardResponse, ClientAwardDelete
from app.utilities.auth.auth_handler import Permissions, check_jwt_client_with_client
from app.models.uploads import UploadType

class AwardEventRouter(APIRoute):

    event_type = 1

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request):
            response = await original_route_handler(request)
            if response.status_code == 200 and request.method in ['POST', 'PUT', 'DELETE']:
                await ProgramEventActions.create_event_from_route(self, request, response)
            return response

        return custom_route_handler

router = APIRouter(prefix="/clients/{client_uuid}", tags=["Client Awards"], route_class=AwardEventRouter)


@router.get("/awards")
async def get_awards(
    client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
    client_uuid: str,
    query_params: dict = Depends(default_query_params)
) -> Page[ClientAwardResponse]:
    await check_jwt_client_with_client(client_uuid_jwt, client_uuid)
    return await ClientAwardActions.get_client_awards(client_uuid, query_params)


@router.get("/awards/{client_award_9char}", response_model=ClientAwardResponse)
async def get_award(
    client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
    client_uuid: str,
    client_award_9char: str
):
    await check_jwt_client_with_client(client_uuid_jwt, client_uuid)
    return await ClientAwardActions.get_award(client_uuid, client_award_9char)


@router.get(
        "/awards/{client_award_9char}/upload",
        dependencies=[Depends(verify_client_award)]
    )
async def get_award_upload_url(
    client_uuid: str,
    client_award_9char: str,
    file_name: str,
    upload_type: UploadType
):
    return await ClientAwardActions.get_upload_url(
        client_uuid,
        client_award_9char,
        file_name,
        upload_type.value
    )


@router.post("/awards", response_model=list[ClientAwardResponse] | ClientAwardResponse)
async def create_award(
    client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
    client_uuid: str,
    awards: list[ClientAwardCreate] | ClientAwardCreate
):
    await check_jwt_client_with_client(client_uuid_jwt, client_uuid)
    return await ClientAwardActions.create_award(client_uuid, awards)


@router.put("/awards/{client_award_9char}", response_model=ClientAwardResponse)
async def update_award(
    client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
    client_uuid: str,
    client_award_9char: str,
    award_updates: ClientAwardUpdate
):
    await check_jwt_client_with_client(client_uuid_jwt, client_uuid)
    return await ClientAwardActions.update_award(client_uuid, client_award_9char, award_updates)


# this should only work if there is no programs or segments associated with the award
@router.delete("/awards/{client_award_9char}", response_model=ClientAwardDelete|DeleteWarning)
async def delete_award(
    client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
    client_uuid: str,
    client_award_9char: str
):
    await check_jwt_client_with_client(client_uuid_jwt, client_uuid)
    #TODO: add check for programs
    return await ClientAwardActions.delete_award(client_uuid, client_award_9char)
