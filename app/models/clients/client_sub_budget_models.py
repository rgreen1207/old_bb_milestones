from app.routers.v1.v1CommonRouting import ExceptionHandling

class StaticBudget:

    valid_child_type = [0, 1, 2]

    async def create_budget(new_budget, parent):
        if parent.value - new_budget.value < 0:
            return await ExceptionHandling.custom405("Parent budget does not have funds for new budget. Please add funds to parent budget and try again.")
        else:
            parent.value -= new_budget.value
        return new_budget, parent
    
    async def budget_expenditure(budget, expenditure):
        if budget.value - expenditure > 0:
            budget.value -= expenditure
            return budget.value
        else:
            return await ExceptionHandling.custom405("Not enough funds for expenditure.")

class PassthruNoCap:

    valid_child_type = [1, 2]

    @classmethod
    async def create_budget(self, new_budget, parent):
        if new_budget.budget_type in self.valid_child_type:
            new_budget.value = 0
            return new_budget, parent
        else:
            return await ExceptionHandling.custom405(f"Budget type - {new_budget.budget_type} cannot be a child of type 1")

    async def budget_expenditure(budget, parent, expenditure):
        if parent.value - expenditure < 0:
            await ExceptionHandling.custom405(f"Parent budget {parent.name} does not have the funds for an expenditure of {expenditure}")
        else:
            parent.value -= expenditure
            return budget, parent
        
class PassthruCap:

    valid_child_type = [1, 2]

    @classmethod
    async def create_budget(self, new_budget, parent):
        if new_budget.budget_type in self.valid_child_type:
            new_budget.value = -abs(new_budget.value)
            return new_budget, parent
        else:
            return await ExceptionHandling.custom405(f"Budget type - {new_budget.budget_type} cannot be a child of type 2")

    async def budget_expenditure(budget, parent, expenditure):
        if budget.value + expenditure > 0 or parent.value - expenditure < 0:
            return await ExceptionHandling.custom405("Parent budget does not have funds for new budget. Please add funds to parent budget and try again.")
        else: 
            budget.value += expenditure
            parent.value -= expenditure
            if parent.value < 0:
                return await ExceptionHandling.custom405(f"Parent budget {parent.name} does not have the funds for an expenditure of {expenditure}")
            return budget, parent

budget_types = {
    0: StaticBudget,
    1: PassthruNoCap,
    2: PassthruCap
}
