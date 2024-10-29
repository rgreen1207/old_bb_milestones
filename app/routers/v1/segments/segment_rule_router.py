from typing import Annotated
from fastapi import APIRouter, Depends
from app.routers.v1.pagination import Page
from app.routers.v1.dependencies import default_query_params
from app.utilities.auth.auth_handler import Permissions
from app.models.base_class import DeleteWarning
from app.actions.segments.rules import SegmentRuleActions
from app.models.segments import SegmentRuleUpdate, SegmentRuleCreate, SegmentRuleResponse, SegmentRuleDelete

router = APIRouter(
    prefix="/clients/{client_uuid}/programs/{program_9char}/segments/{segment_9char}",
    tags=["Client Program Segment Rules"]
)

def path_params(client_uuid: str, program_9char: str, segment_9char: str, rule_9char: str=None):
    return {
        "client_uuid": client_uuid,
        "program_9char": program_9char,
        "segment_9char": segment_9char,
        "rule_9char": rule_9char
    }


@router.get("/rules", response_model=Page[SegmentRuleResponse])
async def get_rules(
    client_uuid: Annotated[str, Depends(Permissions(level="2"))],
    path_params: dict = Depends(path_params),
    query_params: dict = Depends(default_query_params)
):
    return await SegmentRuleActions.get_all_segment_rules(path_params, query_params)


@router.get("/rules/{rule_9char}", response_model=SegmentRuleResponse)
async def get_rule(
    client_uuid: Annotated[str, Depends(Permissions(level="2"))],
    path_params: dict = Depends(path_params),
):
    return await SegmentRuleActions.get_segment_rule(path_params)


@router.post("/rules", response_model=(list[SegmentRuleResponse] | SegmentRuleResponse))
async def create_rule(
    rules: (list[SegmentRuleCreate] | SegmentRuleCreate),
    client_uuid: Annotated[str, Depends(Permissions(level="2"))],
    program_uuid: str = Depends(SegmentRuleActions.get_program_uuid),
    path_params: dict = Depends(path_params),
):
    return await SegmentRuleActions.create_rules(rules, path_params, program_uuid)


@router.put("/rules/{rule_9char}", response_model=SegmentRuleResponse)
async def update_rule(
    rule_updates: SegmentRuleUpdate,
    client_uuid: Annotated[str, Depends(Permissions(level="2"))],
    path_params: dict = Depends(path_params)
):
    return await SegmentRuleActions.update_rule(rule_updates, path_params)


@router.delete("/rules/{rule_9char}", response_model=SegmentRuleDelete|DeleteWarning)
async def delete_rule(
    client_uuid: Annotated[str, Depends(Permissions(level="2"))],
    path_params: dict = Depends(path_params),
):
    return await SegmentRuleActions.delete_rule(path_params)
