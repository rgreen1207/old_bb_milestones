from .client_router import router as client_router
from .client_award_router import router as awards_router
from .client_budget_router import router as budgets_router
from .client_user_router import router as users_router
from fastapi import APIRouter

v1_clients_router = APIRouter()
v1_clients_router.include_router(client_router)
v1_clients_router.include_router(awards_router)
v1_clients_router.include_router(budgets_router)
v1_clients_router.include_router(users_router)
