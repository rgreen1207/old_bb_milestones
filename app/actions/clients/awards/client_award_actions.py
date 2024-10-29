from app.exceptions import ExceptionHandling
from app.actions.base_actions import BaseActions
from app.actions.upload import UploadActions
from app.models.clients.client_award_models import ClientAwardModelDB, ClientAwardUpdate
from app.models.programs import ProgramAwardModelDB


class ClientAwardActions:

    @staticmethod
    async def to_award_db_model(client_uuid: str, award_data):
        return ClientAwardModelDB(client_uuid=client_uuid, **award_data.__dict__)

    @staticmethod
    async def get_client_awards(client_uuid: str, query_params: dict):
        return await BaseActions.get_all_where(
            ClientAwardModelDB,
            [ClientAwardModelDB.client_uuid == client_uuid],
            query_params
        )

    @staticmethod
    async def get_award(client_uuid: str, client_award_9char: str):
        return await BaseActions.get_one_where(
            ClientAwardModelDB,
            [
                ClientAwardModelDB.client_award_9char == client_award_9char,
                ClientAwardModelDB.client_uuid == client_uuid
            ]
        )

    @classmethod
    async def get_upload_url(cls, client_uuid, client_award_9char, file_name, upload_type):
        if upload_type == "image":
            return await UploadActions.generate_upload_url(upload_type, file_name, client_uuid, client_award_9char)

        raise ExceptionHandling.custom400(f"Upload type {upload_type} is not supported")

    @staticmethod
    async def check_if_award_exists_by_name(client_uuid: str, name: str, error=True):
        award = await BaseActions.check_if_exists(
            ClientAwardModelDB,
            [
                ClientAwardModelDB.name == name,
                ClientAwardModelDB.client_uuid == client_uuid
            ]
        )
        if award and error:
            return await ExceptionHandling.custom409(f"Client award with name '{name}' already exists.")
        elif award and not error:
            return award
        else:
            return None

    @classmethod
    async def create_award(cls, client_uuid: str, award_obj):
        if isinstance(award_obj, list):
            to_create = []
            return_list = []
            for award in award_obj:
                existing_award = await ClientAwardActions.check_if_award_exists_by_name(client_uuid, award.name, False)
                if existing_award:
                    return_list.append(existing_award)
                else:
                    to_create.append(await ClientAwardActions.to_award_db_model(client_uuid, award))
            if len(to_create) > 0:
                return_list.extend(await BaseActions.create(to_create))
            return return_list
        award = await ClientAwardActions.check_if_award_exists_by_name(client_uuid, award_obj.name, False)
        if award:
            return award
        return await BaseActions.create(await cls.to_award_db_model(client_uuid, award_obj))


    @classmethod
    async def update_award(
        cls,
        client_uuid: str,
        client_award_9char: str,
        award_updates: ClientAwardUpdate
    ):
        if award_updates.name:
            await cls.check_if_award_exists_by_name(client_uuid, award_updates.name)
        if award_updates.hero_image:
            award_updates.hero_image, _ = await UploadActions.verify_upload_file("image", award_updates.hero_image)
            # TODO: add s3 query to check if file exists and is valid
        return await BaseActions.update(
            ClientAwardModelDB,
            [
                ClientAwardModelDB.client_award_9char == client_award_9char,
                ClientAwardModelDB.client_uuid == client_uuid
            ],
            award_updates
        )

    @staticmethod
    async def delete_award(client_uuid: str, client_award_9char: str):
        program = await BaseActions.get_one_where(
            ProgramAwardModelDB,
            [
                ProgramAwardModelDB.client_award_9char == client_award_9char,
                ProgramAwardModelDB.client_uuid == client_uuid
            ],
            False
        )
        if program:
            return await ExceptionHandling.custom409(
                f"Cannot delete client award {client_award_9char} is currently in use by program: {program.name}."
            )
        return await BaseActions.delete_one(
            ClientAwardModelDB,
            [
                ClientAwardModelDB.client_award_9char == client_award_9char,
                ClientAwardModelDB.client_uuid == client_uuid
            ]
        )

class AwardEventActions:

    async def create_program_event(new_event, request, response):
        return new_event
        #currently no method to retrieve the program_9char, program_uuid, and segment_9char from client_awards