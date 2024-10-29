from fastapi import APIRouter, Depends
from app.routers.v1.pagination import Page
from app.routers.v1.dependencies import default_query_params
from app.models.base_class import DeleteWarning
from app.models.segments import SegmentDesignUpdate, SegmentDesignResponse, SegmentDesignCreate, SegmentDesignDelete
from app.actions.segments.design import SegmentDesignActions


router = APIRouter(prefix="/clients/{client_uuid}/programs/{program_9char}/segments/{segment_9char}", tags=["Client Program Segment Designs"])

def path_params(client_uuid: str, program_9char: str, segment_9char: str, design_9char: str=None):
    return {
        "client_uuid": client_uuid,
        "program_9char": program_9char,
        "segment_9char": segment_9char,
        "design_9char": design_9char
    }


@router.get("/designs", response_model=Page[SegmentDesignResponse])
async def get_segment_designs(
    path_params: dict = Depends(path_params),
    query_params: dict = Depends(default_query_params)
):
    return await SegmentDesignActions.get_all_segment_designs(path_params, query_params)


@router.get("/designs/{design_9char}", response_model=SegmentDesignResponse)
async def get_segment_design(
    path_params: dict = Depends(path_params)
):
    return await SegmentDesignActions.get_segment_design(path_params)


@router.post("/designs", response_model=(list[SegmentDesignResponse] | SegmentDesignResponse))
async def create_segment_design(
    designs: (list[SegmentDesignCreate] | SegmentDesignCreate),
    program_uuid: str = Depends(SegmentDesignActions.get_program_uuid),
    path_params: dict = Depends(path_params)
):
    return await SegmentDesignActions.create_designs(designs, path_params, program_uuid)


@router.put("/designs/{design_9char}", response_model=SegmentDesignResponse)
async def update_segment_design(
    design_updates: SegmentDesignUpdate,
    path_params: dict = Depends(path_params),
):
    return await SegmentDesignActions.update_design(design_updates, path_params)


@router.delete("/designs/{design_9char}", response_model=SegmentDesignDelete|DeleteWarning)
async def delete_segment_design(
    path_params: dict = Depends(path_params),
):
    return await SegmentDesignActions.delete_design(path_params)
