from app.routers.v1.v1CommonRouting import CommonRoutes, ExceptionHandling
from app.models.clients import ClientBudgetModelDB
from app.models.clients.client_sub_budget_models import budget_types
from app.actions.helper_actions import HelperActions
from app.actions.base_actions import BaseActions

class ClientSubBudgetActions:

    @staticmethod
    async def get_sub_budget_type(budget):
        return budget_types[budget.budget_type]

    @classmethod
    async def create_sub_budget(cls, new_budget, parent):
        try:
            budget_class = await cls.get_sub_budget_type(new_budget)
            budget, parent = await budget_class.create_budget(new_budget, parent)
            budget = ClientBudgetModelDB(
                **new_budget.dict(),
                uuid = await HelperActions.generate_UUID(),
                client_uuid = parent.client_uuid
            )
            budget.budget_9char = await HelperActions.generate_9char()
        except Exception as e:
            return await ExceptionHandling.custom405(f"Unable to complete creation of budget: {new_budget.name}.\nReason: {e.detail}")
        else: #if no exception is generated, then commit changes to db
            budget = await CommonRoutes.create_one_or_many(budget)
            await BaseActions.update_without_lookup(parent)
            return budget


    @staticmethod
    async def get_all_sub_budgets(budget_9char, client_uuid):
        return await BaseActions.get_all_where(ClientBudgetModelDB, [ClientBudgetModelDB.client_uuid == client_uuid, ClientBudgetModelDB.parent_9char == budget_9char], params=None, check404=False, pagination=False)

    @classmethod
    async def sub_budget_expenditure(cls, budget, parent, expenditure):
        budget_class = await cls.get_sub_budget_type(budget)
        if budget.budget_type != 0:
            static_parent, passthroughCap = await cls.find_next_static_budget(budget)
            for item in passthroughCap:
                item.value += expenditure
                if item.value + expenditure > 0:
                    return await ExceptionHandling.custom405(f"Not enough passthrough budget in {item.name}")
            budget, static_parent = await budget_class.budget_expenditure(budget, static_parent, expenditure)
            return budget.value, static_parent, passthroughCap
        else:
            budget = await budget_class.budget_expenditure(budget, expenditure)
            return budget

    @staticmethod
    async def valid_child_budget(budget, parent):
        return budget.budget_type in budget_types[parent.budget_type].valid_child_type

    @staticmethod
    async def find_next_static_budget(budget):
        budgetExpendList = []
        while budget.budget_type != 0:
            budget = await BaseActions.check_if_exists(ClientBudgetModelDB, [ClientBudgetModelDB.budget_9char == budget.parent_9char,
                        ClientBudgetModelDB.client_uuid == budget.client_uuid])
            if budget.budget_type == 2:
                budgetExpendList.append(budget)
        return budget, budgetExpendList
