from typing import Annotated
from fastapi import APIRouter, Depends
from app.utilities.auth.auth_handler import Permissions, check_jwt_client_with_client
from app.routers.v1.pagination import Page
from app.routers.v1.dependencies import default_query_params
from app.models.base_class import DeleteWarning
from app.models.segments import SegmentUpdate, SegmentCreate, SegmentResponse, SegmentDelete
from app.actions.segments import SegmentActions


router = APIRouter(
    prefix="/clients/{client_uuid}/programs/{program_9char}",
    tags=["Client Program Segments"]
)


def path_params(client_uuid: str, program_9char: str, segment_9char: str=None):
    return {
        "client_uuid": client_uuid,
        "program_9char": program_9char,
        "segment_9char": segment_9char
    }


@router.get("/segments", response_model=Page[SegmentResponse])
async def get_segments(
    client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
    path_params: dict = Depends(path_params),
    query_params: dict = Depends(default_query_params)
):
    await check_jwt_client_with_client(client_uuid_jwt, path_params["client_uuid"])
    return await SegmentActions.get_all_segments(path_params, query_params)


@router.get("/segments/{segment_9char}", response_model=SegmentResponse)
async def get_segment(
    client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
    path_params: dict = Depends(path_params),
):
    await check_jwt_client_with_client(client_uuid_jwt, path_params["client_uuid"])
    return await SegmentActions.get_segment(path_params)


@router.post("/segments", response_model=(list[SegmentResponse] | SegmentResponse))
async def create_segment(
    client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
    segments: (list[SegmentCreate] | SegmentCreate),
    path_params: dict = Depends(path_params),
):
    await check_jwt_client_with_client(client_uuid_jwt, path_params["client_uuid"])
    return await SegmentActions.create_segment(segments, path_params)


@router.put("/segments/{segment_9char}", response_model=SegmentResponse)
async def update_segment(
    client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
    segment_updates: SegmentUpdate,
    path_params: dict = Depends(path_params)
):
    await check_jwt_client_with_client(client_uuid_jwt, path_params["client_uuid"])
    return await SegmentActions.update_segment(path_params, segment_updates)


@router.delete("/segments/{segment_9char}", response_model=SegmentDelete|DeleteWarning)
async def delete_segment(
    client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
    path_params: dict = Depends(path_params)
):
    await check_jwt_client_with_client(client_uuid_jwt, path_params["client_uuid"])
    return await SegmentActions.delete_segment(path_params)
