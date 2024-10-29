from .program_admin_router import router as admin_router
from .program_award_router import router as award_router
from .program_event_router import router as event_router
from .program_message_router import router as message_router
from .program_router import router as program_router
from .program_rule_router import router as rule_router
from fastapi import APIRouter

v1_program_router = APIRouter()
v1_program_router.include_router(program_router)
v1_program_router.include_router(admin_router)
v1_program_router.include_router(award_router)
v1_program_router.include_router(event_router)
v1_program_router.include_router(rule_router)
v1_program_router.include_router(message_router)
