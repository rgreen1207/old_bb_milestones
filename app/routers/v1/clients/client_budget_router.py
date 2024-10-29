from typing import Optional, Annotated, Callable
from fastapi import APIRouter, Depends
from fastapi.routing import APIRoute
from app.actions.programs.events.program_event_actions import ProgramEventActions
from app.routers.v1.pagination import Page
from app.routers.v1.dependencies import default_query_params
from app.actions.clients.budgets import ClientBudgetActions
from app.models.base_class import DeleteWarning
from app.models.clients import ClientBudgetUpdate, ClientBudgetCreate, ClientBudgetModel, BudgetResponse, ClientBudgetShortExpand, ClientBudgetExpanded, DeleteResponse
from app.utilities.auth.auth_handler import Permissions, check_jwt_client_with_client

class BudgetEventRouter(APIRoute):

    event_type = 4

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request):
            response = await original_route_handler(request)
            if response.status_code == 200 and request.method in ['POST', 'PUT', 'DELETE']:
                await ProgramEventActions.create_event_from_route(self, request, response)
            return response

        return custom_route_handler

router = APIRouter(prefix="/clients/{client_uuid}", tags=["Client Budgets"], route_class=BudgetEventRouter)

@router.get("/budgets", response_model=Page[ClientBudgetModel])
async def get_budgets(
    client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
    client_uuid: str,
    query_params=Depends(default_query_params)
):
    await check_jwt_client_with_client(client_uuid_jwt, client_uuid)
    return await ClientBudgetActions.get_all_budgets(client_uuid, query_params)

@router.get(
        "/budgets/{budget_9char}",
        response_model=ClientBudgetShortExpand|ClientBudgetExpanded
    )
async def get_budget(
        client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
        client_uuid: str,
        budget_9char: str,
        expanded: Optional[bool] = False):
    await check_jwt_client_with_client(client_uuid_jwt, client_uuid)
    return await ClientBudgetActions.get_one_budget(budget_9char, client_uuid, expanded)

@router.post("/budgets", response_model=BudgetResponse) #only allowed to create 1 at a time
async def create_budget(
        client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
        client_uuid: str,
        new_budget: ClientBudgetCreate
        ):
    await check_jwt_client_with_client(client_uuid_jwt, client_uuid)
    return await ClientBudgetActions.create_budget(new_budget, client_uuid)

@router.put("/budgets/{budget_9char}") # , response_model=BudgetResponse
async def update_budget(
        client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
        budget_9char: str,
        client_uuid: str,
        budget_updates: ClientBudgetUpdate
        ):
    await check_jwt_client_with_client(client_uuid_jwt, client_uuid)
    return await ClientBudgetActions.update_budget(budget_updates, budget_9char, client_uuid)

# this should only work if there are no programs associated with the budget
@router.delete("/budgets/{budget_9char}", response_model=DeleteResponse|DeleteWarning)
async def delete_budget(
        client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
        budget_9char: str,
        client_uuid: str
        ):
    await check_jwt_client_with_client(client_uuid_jwt, client_uuid)
    response = await ClientBudgetActions.delete_budget(budget_9char, client_uuid)
    return DeleteResponse.format_data(response)
