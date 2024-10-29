from app.exceptions import ExceptionHandling
from app.actions.base_actions import BaseActions
from app.actions.upload import UploadActions
from app.models.segments.segment_award_models import SegmentAwardModelDB

class SegmentAwardActions:

    @staticmethod
    async def get_all_segment_awards(path_params, query_params):
        return await BaseActions.get_all_where(
            SegmentAwardModelDB,
            [
            SegmentAwardModelDB.client_uuid == path_params["client_uuid"],
            SegmentAwardModelDB.program_9char == path_params["program_9char"],
            SegmentAwardModelDB.segment_9char == path_params["segment_9char"]
            ],
            query_params
        )

    @staticmethod
    async def get_segment_award(path_params):
        return await BaseActions.get_one_where(
            SegmentAwardModelDB,
            [
            SegmentAwardModelDB.segment_9char == path_params["segment_9char"],
            SegmentAwardModelDB.client_uuid == path_params["client_uuid"],
            SegmentAwardModelDB.program_9char == path_params["program_9char"],
            SegmentAwardModelDB.segment_award_9char == path_params["segment_award_9char"]
            ]
        )

    @classmethod
    async def get_segment_upload_url(cls, path_params: dict, file_name: str, upload_type: str):
        if upload_type == "image":
            return await UploadActions.generate_upload_url(
                upload_type,
                file_name,
                path_params.get("client_uuid"),
                path_params.get("segment_award_9char"),
                path_params.get("program_9char"),
                path_params.get("segment_9char")
            )

        raise ExceptionHandling.custom400(f"Upload type {upload_type} is not supported")

    @classmethod
    async def create_segment_award(cls, segment_awards, path_params):
        if isinstance(segment_awards, list):
            to_create = []
            return_list = []
            award_models = [SegmentAwardModelDB(
                **segment_award.dict(),
                client_uuid = path_params["client_uuid"],
                program_9char = path_params["program_9char"],
                segment_9char = path_params["segment_9char"],
                program_award_9char = path_params["program_award_9char"],
            ) for segment_award in segment_awards]
            for award in award_models:
                existing_award = await cls.check_if_award_exists(award.uuid)
                if existing_award:
                    return_list.append(existing_award)
                else:
                    to_create.append(award)
            if to_create:
                return_list.extend(await BaseActions.create(to_create))
            return return_list

        award_model = SegmentAwardModelDB(
            **segment_awards.dict(),
                client_uuid = path_params["client_uuid"],
                program_9char = path_params["program_9char"],
                segment_9char = path_params["segment_9char"],
                program_award_9char = path_params["program_award_9char"],
        )
        existing_award = await cls.check_if_award_exists(award_model.uuid)
        if existing_award:
            return existing_award
        return await BaseActions.create(award_model)

    @classmethod
    async def update_segment_award(cls, path_params, segment_award_updates):
        if segment_award_updates.name:
            await cls.check_if_award_name_exists(path_params, segment_award_updates.name)
        if segment_award_updates.hero_image:
            segment_award_updates.hero_image, _ = await UploadActions.verify_upload_file("image", segment_award_updates.hero_image)
            # TODO: add s3 query to check if file exists and is valid
        return await BaseActions.update(
            SegmentAwardModelDB,
            [
            SegmentAwardModelDB.segment_9char == path_params["segment_9char"],
            SegmentAwardModelDB.client_uuid == path_params["client_uuid"],
            SegmentAwardModelDB.program_9char == path_params["program_9char"],
            SegmentAwardModelDB.segment_award_9char == path_params["segment_award_9char"]
            ],
            segment_award_updates
        )

    @staticmethod
    async def delete_segment_award(path_params):
        return await BaseActions.delete_one(
            SegmentAwardModelDB,
            [
            SegmentAwardModelDB.segment_9char == path_params["segment_9char"],
            SegmentAwardModelDB.client_uuid == path_params["client_uuid"],
            SegmentAwardModelDB.program_9char == path_params["program_9char"],
            SegmentAwardModelDB.segment_award_9char == path_params["segment_award_9char"]
            ]
        )

    @staticmethod
    async def check_if_award_name_exists(path_params, name):
        # check using cleint id, program id, segment id, and award name
        award = await BaseActions.check_if_exists(
            SegmentAwardModelDB,
            [
            SegmentAwardModelDB.client_uuid == path_params["client_uuid"],
            SegmentAwardModelDB.program_9char == path_params["program_9char"],
            SegmentAwardModelDB.segment_9char == path_params["segment_9char"],
            SegmentAwardModelDB.name == name
            ]
        )
        if award:
            return await ExceptionHandling.custom409(f"Program award with name '{name}' already exists.")

    @staticmethod
    async def check_if_award_exists(award_uuid: str):
        award = await BaseActions.check_if_exists(
            SegmentAwardModelDB,
            [
                SegmentAwardModelDB.uuid == award_uuid
            ]
        )
        return award
