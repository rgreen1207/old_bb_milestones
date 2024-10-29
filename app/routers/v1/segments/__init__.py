from fastapi import APIRouter
from .segment_router import router as segment_router
from .segment_award_router import router as awards_router
from .segment_design_router import router as design_router
from .segment_rule_router import router as rules_router
from .segment_message_router import router as message_router

v1_segments_router = APIRouter()
v1_segments_router.include_router(segment_router)
v1_segments_router.include_router(awards_router)
v1_segments_router.include_router(design_router)
v1_segments_router.include_router(rules_router)
v1_segments_router.include_router(message_router)
