import json
from datetime import datetime
from app.routers.v1.v1CommonRouting import CommonRoutes, ExceptionHandling
from app.utilities import SHA224Hash
from app.actions.helper_actions import HelperActions
from app.actions.clients import ClientActions
from app.models.clients import ClientBudgetModelDB, ClientBudgetExpanded, ClientModelDB, ClientBudgetShortExpand
from app.models.programs import ProgramModelDB
from app.models.segments import SegmentModelDB
from .client_sub_budget_actions import ClientSubBudgetActions
from app.actions.base_actions import BaseActions

class ClientBudgetActions:

    @staticmethod
    async def default_budget_name(client_uuid):
        client_name = await ClientActions.get_client_name(client_uuid)
        budgetCreationTime = datetime.now(datetime.UTC).strftime("%m/%d/%Y %H:%M:%S %Z")
        return f"New {client_name} Budget (created: {budgetCreationTime})"

    @staticmethod
    async def check_for_existing_budget_by_name(budget, client_uuid):
        existingBudget = await BaseActions.check_if_exists(ClientBudgetModelDB, [
            ClientBudgetModelDB.name == budget.name,
            ClientBudgetModelDB.client_uuid == client_uuid
            ])
        if existingBudget:
            message = f"A budget with name '{budget.name}' already exists."
            await ExceptionHandling.custom405(message)
        else:
            return budget.name

    @staticmethod
    async def get_all_budgets(client_uuid: str, query_params: dict):
        return await BaseActions.get_all_where(
            ClientBudgetModelDB,
            [
                ClientBudgetModelDB.client_uuid == client_uuid
            ],
            query_params
        )

    @staticmethod #this goes from child --> parent
    async def get_budget_by_9char_and_client_uuid(budget_9char, client_uuid, check404=False):
        return await BaseActions.get_one_where(ClientBudgetModelDB, [
            ClientBudgetModelDB.budget_9char == budget_9char,
            ClientBudgetModelDB.client_uuid == client_uuid
        ], check404)

    @staticmethod #this goes from parent --> children
    async def get_budgets_by_parent_9char(budget):
        return await BaseActions.get_all_where(ClientBudgetModelDB, [
            ClientBudgetModelDB.parent_9char == budget.budget_9char,
            ClientBudgetModelDB.client_uuid == budget.client_uuid
        ], params=None, check404=False, pagination=False)

    @staticmethod
    async def get_all_subbudgets_value(subbudgets):
        total = 0
        for budget in subbudgets:
            total += abs(budget.value)
        return total

    @classmethod
    async def validate_new_budget_name(cls, new_budget, client_uuid):
        if new_budget.name:
            return await cls.check_for_existing_budget_by_name(new_budget, client_uuid)
        return await cls.default_budget_name(client_uuid)

    @classmethod
    async def check_for_valid_parent(cls, parent_9char, client_uuid):
        parent = await cls.get_budget_by_9char_and_client_uuid(parent_9char, client_uuid)
        if not parent:
            return await ExceptionHandling.custom405("No parent budget with specified 9char has been found.")
        return parent

    @classmethod
    async def get_one_budget(cls, budget_9char: str, client_uuid: str, expanded):
        budget = await cls.get_budget_by_9char_and_client_uuid(budget_9char, client_uuid, True)
        subbudgets = await cls.get_all_subbudgets(budget)
        client = await BaseActions.get_one_where(ClientModelDB, [ClientModelDB.uuid == client_uuid], False)
        if expanded:
            budget = ClientBudgetExpanded.from_orm(budget)
            budget.client = client
            budget.subbudgets_expanded = subbudgets
        else:
            budget = ClientBudgetShortExpand.from_orm(budget)
            value =  await cls.get_all_subbudgets_value(subbudgets)
            budget.subbudgets = {
                "subbudgets": len(subbudgets),
                "value": value
            }
            budget.client = client.name
        return budget

    @classmethod
    async def get_all_subbudgets(cls, budget):
        stack = []
        #get the 1st level of children budgets
        budgets = await cls.get_budgets_by_parent_9char(budget)
        for i in budgets:
            stack.append(i)
        return_budgets = []
        while stack:
            budget = stack.pop()
            budgets = await cls.get_budgets_by_parent_9char(budget)
            for i in budgets:
                stack.append(i) if i else None
            return_budgets.append(budget) if budget else None
        return return_budgets

    @classmethod
    async def create_budget(cls, new_budget, client_uuid: str):
        new_budget.name = await cls.validate_new_budget_name(new_budget, client_uuid)
        if new_budget.budget_type in [1, 2] and new_budget.parent_9char is None:
                return await ExceptionHandling.custom405("A passthrough budget must have a parent budget.")
        elif new_budget.parent_9char:
            parent = await cls.check_for_valid_parent(new_budget.parent_9char, client_uuid)
            return await ClientSubBudgetActions.create_sub_budget(new_budget, parent)
        else:
            budget = ClientBudgetModelDB(
                **new_budget.dict(),
                uuid= SHA224Hash(),
                client_uuid=client_uuid
            )

            #reason why this isnt part of declaration above: https://stackoverflow.com/questions/18950054/class-method-generates-typeerror-got-multiple-values-for-keyword-argument
            budget.budget_9char = await HelperActions.generate_9char()
            return await CommonRoutes.create_one_or_many(budget)

    @classmethod
    async def update_budget(cls, budget_updates, budget_9char: str, client_uuid: str):
        budget = await cls.get_budget_by_9char_and_client_uuid(budget_9char, client_uuid)
        """
        if a budget has a program attached, a child, or an expenditure it cannot be modified except for name and value
        """
        parent_9char = budget_updates.parent_9char if budget_updates.parent_9char else budget.parent_9char
        parent = await cls.check_for_valid_parent(parent_9char, client_uuid) if parent_9char else None
        if budget_updates.name:
            await cls.check_for_existing_budget_by_name(budget_updates, budget.client_uuid)
        if budget_updates.parent_9char or budget_updates.budget_type:

            if budget_updates.parent_9char == budget_9char:
                return await ExceptionHandling.custom405("Cannot set same value for parent_9char and budget_9char.")
            else:
                child_budget = budget_updates if budget_updates.budget_type else budget
                if not await ClientSubBudgetActions.valid_child_budget(child_budget, parent):
                    return await ExceptionHandling.custom405("Unable to set new parent budget.")
                else:
                    budget.budget_type = budget_updates.budget_type
        if "value" in budget_updates.dict(exclude_unset=True):
            if budget.budget_type != 0 and await ClientSubBudgetActions.valid_child_budget(budget, parent):
                budget_updates.value, parent, passthroughList = await ClientSubBudgetActions.sub_budget_expenditure(budget, parent, budget_updates.value)
            else:
                budget_updates.value = await ClientSubBudgetActions.sub_budget_expenditure(budget, None, budget_updates.value)
        update_budget = budget_updates.dict(exclude_unset=True)
        for k,v in update_budget.items():
            setattr(budget, k, v)
        if budget.budget_type != 0 and ("value" in budget_updates.dict(exclude_unset=True)):
            budget = await BaseActions.update_without_lookup(budget)
            parent = await BaseActions.update_without_lookup(parent)
            if not passthroughList:
                return {"updated": budget, "static_parent": parent}
            else:
                passthroughList = await BaseActions.update_without_lookup(passthroughList)
                return {"updated": budget, "static_parent": parent, "passthrough_budgets_affected": passthroughList}
        else:
            return await BaseActions.update_without_lookup(budget)

    @classmethod
    async def delete_budget(cls, budget_9char: str, client_uuid: str):
        budget = await cls.get_budget_by_9char_and_client_uuid(budget_9char, client_uuid)
        sub_budgets = await ClientSubBudgetActions.get_all_sub_budgets(budget_9char, client_uuid)
        budget_in_use, message = await cls.budget_in_use(budget_9char, client_uuid)
        if sub_budgets or budget_in_use:
            message = f"Unable to delete budget named: {budget.name}. {message}" if message else f"Unable to delete budget named: {budget.name}."
            return await ExceptionHandling.custom405(message)
        elif budget.budget_type == 0 and budget.parent_9char is not None:
            parent = await cls.get_budget_by_9char_and_client_uuid(budget.parent_9char, client_uuid)
            parent.value += budget.value
            return [await BaseActions.delete_without_lookup(budget), await BaseActions.update_without_lookup(parent)]
        else:
            return await BaseActions.delete_without_lookup(budget)

    @classmethod
    async def budget_in_use(cls, budget_9char: str, client_uuid: str) -> bool:
        program = await cls.get_program_by_budget(budget_9char, client_uuid)
        if program:
            return (True, f"Budget is in use by program: {program.name}.")
        else:
            return False, None

    @staticmethod
    async def get_program_by_budget(budget_9char: str, client_uuid: str):
        return await BaseActions.get_one_where(ProgramModelDB, [
            ProgramModelDB.budget_9char == budget_9char,
            ProgramModelDB.client_uuid == client_uuid
        ], check404=False)

    @staticmethod
    async def get_segment_by_budget(budget_9char: str, client_uuid: str):
        return await BaseActions.get_one_where(SegmentModelDB, [
            SegmentModelDB.budget_9char == budget_9char,
            SegmentModelDB.client_uuid == client_uuid
        ], check404=False)


class ClientBudgetEventActions:

    async def create_program_event(new_event, request, response):
        event_data = json.loads(new_event.event_data)
        if request.method == 'PUT':
            if 'updated' in event_data:
                budget_9char = event_data['updated']['budget_9char']
            else:
                budget_9char = event_data['budget_9char']
        elif request.method == "DELETE":
            try:
                budget_9char = event_data['Deleted']['budget_9char']
            except TypeError:
                budget_9char = event_data[0]['Deleted']['budget_9char']
        else: #created budgets
            budget_9char = event_data['budget_9char']

        program = await ClientBudgetActions.get_program_by_budget(budget_9char, new_event.client_uuid)
        new_event.program_uuid = program.uuid if program else None
        new_event.program_9char = program.program_9char if program else None
        segment = await ClientBudgetActions.get_segment_by_budget(budget_9char, new_event.client_uuid)
        new_event.segment_uuid = segment.uuid if segment else None
        return new_event
