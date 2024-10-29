import json
from app.actions.base_actions import BaseActions
from app.actions.helper_actions import HelperActions
from app.models.programs.program_models import ProgramModelDB
from app.models.programs.program_event_models import ProgramEventModelDB
from app.utilities import SHA224Hash
from app.actions.helper_actions import HelperActions
from app.actions.messages.message_actions import ClientMessageEventActions
from app.actions.clients.budgets import ClientBudgetEventActions
from app.actions.clients.awards.client_award_actions import AwardEventActions

class ProgramEventActions:

    @classmethod
    async def create_event_from_route(cls, program_router, request, response):
        new_event = ProgramEventModelDB(
            uuid=SHA224Hash(),
            event_9char=await HelperActions.generate_9char(),
            client_uuid=request.path_params["client_uuid"] if "client_uuid" in request.path_params else None,
            event_data = response.body.decode("utf-8"),
            event_type = program_router.event_type,
            status = response.status_code,
        )
        new_event = await {
            1: AwardEventActions.create_program_event,
            #2: SegmentActions.create_program_event,
            3: ClientMessageEventActions.create_program_event,
            4: ClientBudgetEventActions.create_program_event
        }[new_event.event_type](new_event, request, response)

        new_event.event_data = json.dumps({
            "request_url": request.url.path,
            "request_method": request.method,
            "request_body": json.dumps(json.loads(request._body.decode("utf-8"))) if '_body' in request.__dict__ else None, #double json. to remove the escape characters and save as a str
            "response_status": response.status_code,
            "response_body": response.body.decode("utf-8")
        })
        await BaseActions.create(new_event)




    @staticmethod
    async def get_all_client_events(
        client_uuid, query_params
    ):
        return await BaseActions.get_all_where(
            ProgramEventModelDB,
            [
                ProgramEventModelDB.client_uuid == client_uuid
            ],
            query_params
        )

    @staticmethod
    async def get_all_program_events(
        path_params,
        query_params
    ):
        return await BaseActions.get_all_where(
            ProgramEventModelDB,
            [
                ProgramEventModelDB.client_uuid == path_params["client_uuid"],
                ProgramEventModelDB.program_9char == path_params["program_9char"]
            ],
            query_params
        )

    @staticmethod
    async def get_event(path_params):
        return await BaseActions.get_one_where(
            ProgramEventModelDB,
            [
                ProgramEventModelDB.event_9char == path_params["event_9char"],
                ProgramEventModelDB.client_uuid == path_params["client_uuid"],
                ProgramEventModelDB.program_9char == path_params["program_9char"]
            ]
        )

    @staticmethod
    async def get_program_uuid(program_9char: str):
        return await BaseActions.get_one_where(
            ProgramModelDB.uuid,
            [ProgramModelDB.program_9char == program_9char]
        )

    @staticmethod
    async def create_event(event_obj, path_params, program_uuid):
        if isinstance(event_obj, list):
            event_objs = [ProgramEventModelDB(
                **event.dict(),
                program_uuid = program_uuid,
                client_uuid = path_params["client_uuid"],
                program_9char = path_params["program_9char"],
                event_9char = await HelperActions.generate_9char()
            ) for event in event_obj]
            return await BaseActions.create(event_objs)
        event_obj = ProgramEventModelDB(
            **event_obj.dict(),
            program_uuid = program_uuid,
            client_uuid = path_params["client_uuid"],
            program_9char = path_params["program_9char"],
            event_9char = await HelperActions.generate_9char()
        )
        return await BaseActions.create(event_obj)

    @staticmethod
    async def update_event(event_updates, path_params):
        return await BaseActions.update(
            ProgramEventModelDB,
            [
                ProgramEventModelDB.event_9char == path_params["event_9char"],
                ProgramEventModelDB.client_uuid == path_params["client_uuid"],
                ProgramEventModelDB.program_9char == path_params["program_9char"]
            ],
            event_updates)

    @staticmethod
    async def delete_event(path_params):
        return await BaseActions.delete_one(
            ProgramEventModelDB,
            [
                ProgramEventModelDB.event_9char == path_params["event_9char"],
                ProgramEventModelDB.client_uuid == path_params["client_uuid"],
                ProgramEventModelDB.program_9char == path_params["program_9char"]
            ]
        )
