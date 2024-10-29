from typing import Annotated

from fastapi import APIRouter, Depends
from app.routers.v1.dependencies import default_query_params
from app.routers.v1.pagination import Page
from app.models.base_class import DeleteWarning
from app.models.programs import ProgramRuleCreate, ProgramRuleUpdate, ProgramRuleResponse, ProgramRuleDelete
from app.actions.programs.rule.program_rule_actions import ProgramRuleActions
from app.utilities.auth.auth_handler import Permissions, check_jwt_client_with_client

router = APIRouter(
    prefix="/clients/{client_uuid}/programs/{program_9char}",
    tags=["Client Program Rules"]
)


def path_params(client_uuid: str, program_9char: str, rule_9char: str=None):
    return {
        "client_uuid": client_uuid,
        "program_9char": program_9char,
        "rule_9char": rule_9char
    }


@router.get("/rules", response_model=Page[ProgramRuleResponse])
async def get_rules(
    client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
    path_params: dict = Depends(path_params),
    query_params: dict = Depends(default_query_params)
):
    await check_jwt_client_with_client(client_uuid_jwt, path_params["client_uuid"])
    return await ProgramRuleActions.get_all_rules(path_params, query_params)


@router.get("/rules/{rule_9char}", response_model=ProgramRuleResponse)
async def get_rule(
    client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
    path_params: dict = Depends(path_params)
):
    await check_jwt_client_with_client(client_uuid_jwt, path_params["client_uuid"])
    return await ProgramRuleActions.get_rule(path_params)


@router.post("/rules", response_model=(list[ProgramRuleResponse] | ProgramRuleResponse))
async def create_rule(
    client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
    rules: (list[ProgramRuleCreate] | ProgramRuleCreate),
    path_params: dict = Depends(path_params),
    program_uuid: str = Depends(ProgramRuleActions.get_program_uuid)
):
    await check_jwt_client_with_client(client_uuid_jwt, path_params["client_uuid"])
    return await ProgramRuleActions.create_rule(rules, path_params, program_uuid)


@router.put("/rules/{rule_9char}", response_model=ProgramRuleResponse)
async def update_rule(
    client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
    rule_updates: ProgramRuleUpdate,
    path_params: dict = Depends(path_params)
):
    await check_jwt_client_with_client(client_uuid_jwt, path_params["client_uuid"])
    return await ProgramRuleActions.update_rule(rule_updates, path_params)


@router.delete("/rules/{rule_9char}", response_model=ProgramRuleDelete|DeleteWarning)
async def delete_rule(
    client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
    path_params: dict = Depends(path_params)
):
    await check_jwt_client_with_client(client_uuid_jwt, path_params["client_uuid"])
    return await ProgramRuleActions.delete_rule(path_params)
