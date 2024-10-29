from app.exceptions import ExceptionHandling
from app.actions.base_actions import BaseActions
from app.actions.upload import UploadActions
from app.models.programs.program_award_models import ProgramAwardModelDB, ProgramAwardUpdate
from app.models.segments import SegmentAwardModelDB



class ProgramAwardActions:

    @staticmethod
    async def get_program_awards(path_params: dict, query_params: dict):
        return await BaseActions.get_all_where(
            ProgramAwardModelDB,
            [
                ProgramAwardModelDB.client_uuid == path_params["client_uuid"],
                ProgramAwardModelDB.program_9char == path_params["program_9char"],
            ],
            query_params
        )

    @staticmethod
    async def get_award(path_params: dict):
        return await BaseActions.get_one_where(
            ProgramAwardModelDB,
            [
                ProgramAwardModelDB.client_uuid == path_params["client_uuid"],
                ProgramAwardModelDB.program_9char == path_params["program_9char"],
                ProgramAwardModelDB.program_award_9char == path_params["program_award_9char"]
            ],
        )

    @classmethod
    async def get_upload_url(cls, path_params: dict, file_name: str, upload_type: str):
        if upload_type == "image":
            return await UploadActions.generate_upload_url(
                upload_type,
                file_name,
                path_params.get("client_uuid"),
                path_params.get("program_award_9char"),
                path_params.get("program_9char")
            )

        raise ExceptionHandling.custom400(f"Upload type {upload_type} is not supported")

    @classmethod
    async def create_award(cls,path_params: dict, award_obj):
        if isinstance(award_obj, list):
            to_create = []
            return_list = []
            award_models = [
                ProgramAwardModelDB(
                    **award.dict(),
                    client_uuid=path_params["client_uuid"],
                    program_9char=path_params["program_9char"],
                    client_award_9char=path_params["client_award_9char"]
                ) for award in award_obj]
            for award in award_models:
                existing_award = await cls.check_if_award_exists(award.uuid)
                if existing_award:
                    return_list.append(existing_award)
                else:
                    to_create.append(award)
            if to_create:
                return_list.extend(await BaseActions.create(to_create))
            return return_list

        award_model = ProgramAwardModelDB(
            **award_obj.dict(),
            client_uuid=path_params["client_uuid"],
            program_9char=path_params["program_9char"],
            client_award_9char=path_params["client_award_9char"]
        )
        existing_award = await cls.check_if_award_exists(award_model.uuid)
        if existing_award:
            return existing_award

        return await BaseActions.create(award_model)


    @classmethod
    async def update_award(
        cls,
        path_params: dict,
        award_updates: ProgramAwardUpdate
    ):
        if award_updates.name:
            await cls.check_if_award_exists_by_name(path_params, award_updates.name)
        if award_updates.hero_image:
            award_updates.hero_image, _ = await UploadActions.verify_upload_file("image", award_updates.hero_image)
            # TODO: add s3 query to check if file exists and is valid
        return await BaseActions.update(
            ProgramAwardModelDB,
            [
                ProgramAwardModelDB.client_uuid == path_params["client_uuid"],
                ProgramAwardModelDB.program_9char == path_params["program_9char"],
                ProgramAwardModelDB.program_award_9char == path_params["program_award_9char"]
            ],
            award_updates
        )

    @staticmethod
    async def delete_award(path_params: dict):
        segment =  await BaseActions.get_one_where(
            SegmentAwardModelDB,
            [
                SegmentAwardModelDB.client_uuid == path_params["client_uuid"],
                SegmentAwardModelDB.program_9char == path_params["program_9char"],
                SegmentAwardModelDB.program_award_9char == path_params["program_award_9char"]
            ],
            False
        )
        if segment:
            return await ExceptionHandling.custom409(
                f"Cannot delete program award {path_params.program_award_9char} is currently in use by segment: {segment.name}."
            )
        return await BaseActions.delete_one(
            ProgramAwardModelDB,
            [
                ProgramAwardModelDB.client_uuid == path_params["client_uuid"],
                ProgramAwardModelDB.program_9char == path_params["program_9char"],
                ProgramAwardModelDB.program_award_9char == path_params["program_award_9char"]
            ],
        )

    @staticmethod
    async def check_if_award_exists_by_name(path_params, name: str, error: bool = True):
        award = await BaseActions.check_if_exists(
            ProgramAwardModelDB,
            [
                ProgramAwardModelDB.name == name,
                ProgramAwardModelDB.client_uuid == path_params["client_uuid"],
                ProgramAwardModelDB.program_9char == path_params["program_9char"]
            ]
        )
        if award and error:
            return await ExceptionHandling.custom409(f"Program award with name '{name}' already exists.")
        return award

    @staticmethod
    async def check_if_award_exists(award_uuid: str):
        award = await BaseActions.check_if_exists(
            ProgramAwardModelDB,
            [
                ProgramAwardModelDB.uuid == award_uuid
            ]
        )
        return award
