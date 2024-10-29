from app.models.programs import ProgramModelDB
from app.actions.helper_actions import HelperActions
from app.models.programs.program_event_models import ProgramEventModelDB
from app.models.segments.segment_models import SegmentModelDB
from app.actions.base_actions import BaseActions


class ProgramActions:

    @classmethod
    async def create_program(cls, programs, client_uuid):
        if isinstance(programs, list):
            to_create = []
            to_return = []
            for program in programs:
                program_model = await cls.to_program_model(program, client_uuid)
                existing = await cls.check_if_program_exists(
                    program_model.name, program_model.client_uuid
                )
                if existing:
                    to_return.append(existing)
                else:
                    to_create.append(program_model)
            if to_create:
                to_return.extend(await BaseActions.create(to_create))
            return to_return
        program_model = await cls.to_program_model(programs, client_uuid)
        existing = await cls.check_if_program_exists(
            program_model.name, program_model.client_uuid
        )
        if existing:
            return existing
        return await BaseActions.create(program_model)

    @staticmethod
    async def to_program_model(program, client_uuid):
        return ProgramModelDB(
            **program.dict(),
            client_uuid=client_uuid,
            program_9char = await HelperActions.generate_9char()
        )

    @classmethod
    async def check_if_program_exists(cls, name, client_uuid):
        return await BaseActions.check_if_exists(
            ProgramModelDB,
            [
                ProgramModelDB.name == name,
                ProgramModelDB.client_uuid == client_uuid
            ]
        )

    @classmethod
    async def get_by_program_9char(cls, path_params):
        return await BaseActions.get_one_where(
            ProgramModelDB,
            [
                ProgramModelDB.program_9char == path_params["program_9char"],
                ProgramModelDB.client_uuid == path_params["client_uuid"]
            ]
        )

    @classmethod
    async def get_by_client_uuid(cls, path_params, query_params):
        return await BaseActions.get_all_where(
            ProgramModelDB,
            [
                ProgramModelDB.client_uuid == path_params["client_uuid"]
            ],
            query_params
        )

    @classmethod
    async def update_program(cls, program_updates, path_params):
        return await BaseActions.update(
            ProgramModelDB,
            [
                ProgramModelDB.program_9char == path_params["program_9char"],
                ProgramModelDB.client_uuid == path_params["client_uuid"]
            ],
            program_updates
        )

    @classmethod
    async def check_for_program_event(cls, path_params):
        return await BaseActions.check_if_one_exists(
            ProgramEventModelDB,
            [
                ProgramEventModelDB.client_uuid == path_params["client_uuid"],
                ProgramEventModelDB.program_9char == path_params["program_9char"]
            ]
        )

    @classmethod
    async def check_for_program_segment(cls, path_params):
        return await BaseActions.check_if_one_exists(
            SegmentModelDB,
            [
                SegmentModelDB.client_uuid == path_params["client_uuid"],
                SegmentModelDB.program_9char == path_params["program_9char"]
            ]
        )

    @classmethod
    async def delete_program(cls, path_params):
        segment_check = await cls.check_for_program_segment(path_params)
        if segment_check:
            return {"message":"A segment exists for this program. It cannot be deleted at this time."}

        event_check = await cls.check_for_program_event(path_params)
        if event_check:
            return {"message":"An event exists for this program. It cannot be deleted at this time."}

        return await BaseActions.delete_one(
            ProgramModelDB,
            [
                ProgramModelDB.program_9char == path_params["program_9char"],
                ProgramModelDB.client_uuid == path_params["client_uuid"]
            ]
        )
