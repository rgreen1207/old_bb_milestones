import os
from enum import Enum
from typing import Optional
from fastapi import Query, HTTPException, Request
from app.actions.base_actions import BaseActions
from app.exceptions import ExceptionHandling
from app.models.clients import ClientUserModelDB
from app.models.clients import ClientModelDB
from app.models.clients.client_award_models import ClientAwardModelDB
from app.models.programs import ProgramAwardModelDB
from app.models.segments import SegmentAwardModelDB

class SortOrder(str, Enum):
    ASC = "ASC"
    DESC = "DESC"

    def __str__(self):
        return self.value


def default_query_params(
        request: Request,
        order_by: Optional[str] = "time_created",
        sort: SortOrder = Query(default = SortOrder.DESC)
    ):
    params = {
        "order_by": order_by,
        "sort": str(sort),
        "filters": {},
    }
    for param in request.query_params._dict:
        if param not in params["filters"] and param not in params:
            params["filters"].update({param: request.query_params._dict.get(param)})
    #params.update({"filters": request.query_params._dict} if request.query_params else {})
    return params


async def verify_client_user(user_uuid: str, client_uuid: str):
    user = await BaseActions.check_if_exists(
        ClientUserModelDB,
        [
            ClientUserModelDB.user_uuid == user_uuid,
            ClientUserModelDB.client_uuid == client_uuid
        ]
    )
    await ExceptionHandling.check404(
        user,
        message="The provided user_uuid is not related to the current client"
    )


async def verify_client_uuid(client_uuid: str):
    response = await BaseActions.check_if_exists(
        ClientModelDB,
        [ClientModelDB.uuid == client_uuid]
    )
    if not response:
        raise HTTPException(400, "Client UUID does not exist")


async def verify_client_award(client_uuid: str, client_award_9char: str):
    response =  await BaseActions.check_if_exists(
        ClientAwardModelDB,
        [
            ClientAwardModelDB.client_uuid == client_uuid,
            ClientAwardModelDB.client_award_9char == client_award_9char
        ]
    )
    if not response:
        raise HTTPException(400, "The provided Client Award does not exist")


async def verify_program_award(client_uuid: str, program_award_9char: str):
    response =  await BaseActions.check_if_exists(
        ProgramAwardModelDB,
        [
            ProgramAwardModelDB.client_uuid == client_uuid,
            ProgramAwardModelDB.program_award_9char == program_award_9char
        ]
    )
    if not response:
        raise HTTPException(400, "The provided Program Award does not exist")


async def verify_segment_award(client_uuid: str, segment_award_9char: str):
    response =  await BaseActions.check_if_exists(
        SegmentAwardModelDB,
        [
            SegmentAwardModelDB.client_uuid == client_uuid,
            SegmentAwardModelDB.segment_award_9char == segment_award_9char
        ]
    )
    if not response:
        raise HTTPException(400, "The provided Segment Award does not exist")


def test_mode():
    pm = os.environ.get("ENV")
    pytest = os.environ.get("TEST_MODE", False)
    if pm != "local" and not pytest:
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="No tests running")
    else:
        return True


def is_test_mode():
    pm = os.environ.get("ENV")
    pytest = os.environ.get("TEST_MODE", False)
    if pm != "local" and not pytest:
        return False
    else:
        return True
