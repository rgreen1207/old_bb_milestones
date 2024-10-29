from typing import Annotated
from fastapi import APIRouter, Depends
from app.utilities.auth.auth_handler import Permissions, check_jwt_client_with_client
from app.models.uploads import UploadType
from app.routers.v1.pagination import Page
from app.models.base_class import DeleteWarning
from app.routers.v1.dependencies import default_query_params, verify_segment_award
from app.actions.segments.awards import SegmentAwardActions
from app.models.segments.segment_award_models import SegmentAwardUpdate, SegmentAwardResponse, SegmentAwardCreate, SegmentAwardResponse, ProgramAwardDelete


router = APIRouter(
    prefix="/clients/{client_uuid}/programs/{program_9char}/segments/{segment_9char}",
    tags=["Client Program Segment Awards"]
)


def path_params(
        client_uuid: str,
        program_9char: str,
        segment_9char: str,
        segment_award_9char: str=None,
        program_award_9char: str=None
    ):
    return {
        "client_uuid": client_uuid,
        "program_9char": program_9char,
        "segment_9char": segment_9char,
        "segment_award_9char": segment_award_9char,
        "program_award_9char": program_award_9char
    }

@router.get("/awards", response_model=Page[SegmentAwardResponse])
async def get_segment_awards(
    client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
    path_params: dict = Depends(path_params),
    query_params: dict = Depends(default_query_params)
):
    await check_jwt_client_with_client(client_uuid_jwt, path_params["client_uuid"])
    return await SegmentAwardActions.get_all_segment_awards(path_params, query_params)


@router.get("/awards/{segment_award_9char}", response_model=SegmentAwardResponse)
async def get_segment_award(
    client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
    path_params: dict = Depends(path_params)
):
    await check_jwt_client_with_client(client_uuid_jwt, path_params["client_uuid"])
    return await SegmentAwardActions.get_segment_award(path_params)


@router.get("/awards/{segment_award_9char}/upload", dependencies=[Depends(verify_segment_award)])
async def get_segment_award_upload_url(
    client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
    file_name: str,
    upload_type: UploadType,
    path_params: dict = Depends(path_params)
):
    await check_jwt_client_with_client(client_uuid_jwt, path_params["client_uuid"])
    return await SegmentAwardActions.get_segment_upload_url(path_params, file_name, upload_type.value)


@router.post(
        "/awards/{program_award_9char}",
        response_model=(list[SegmentAwardResponse] | SegmentAwardResponse)
    )
async def create_segment_award(
    client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
    segment_awards: list[SegmentAwardCreate] | SegmentAwardCreate,
    path_params: dict = Depends(path_params)
):
    await check_jwt_client_with_client(client_uuid_jwt, path_params["client_uuid"])
    return await SegmentAwardActions.create_segment_award(segment_awards, path_params)


@router.put("/awards/{segment_award_9char}", response_model=SegmentAwardResponse)
async def update_segment_award(
    client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
    segment_award_updates: SegmentAwardUpdate,
    path_params: dict = Depends(path_params)
):
    await check_jwt_client_with_client(client_uuid_jwt, path_params["client_uuid"])
    return await SegmentAwardActions.update_segment_award(path_params, segment_award_updates)


@router.delete("/awards/{segment_award_9char}", response_model=ProgramAwardDelete|DeleteWarning)
async def delete_segment_award(
    client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
    path_params: dict = Depends(path_params)
):
    await check_jwt_client_with_client(client_uuid_jwt, path_params["client_uuid"])
    return await SegmentAwardActions.delete_segment_award(path_params)
