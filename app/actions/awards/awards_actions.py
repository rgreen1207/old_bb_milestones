from app.actions.base_actions import BaseActions
from app.exceptions import ExceptionHandling
from app.models.award import AwardModelDB, AwardUpdate
from app.actions.upload import UploadActions
from app.models.clients import ClientAwardModelDB

class AwardActions:

    @staticmethod
    async def check_if_award_exists(name, error = True):
        award = await BaseActions.check_if_exists(AwardModelDB, [AwardModelDB.name == name])
        if award and error:
            return await ExceptionHandling.custom409(f"Award with name '{name}' already exists.")
        elif award and not error:
            return award
        else:
            return None

    @staticmethod
    async def get_all_awards(query_params: dict):
        """
        Get all awards from the database
        :params query_params(dict): A dictionary of query parameters
            - order_by(str): The field to sort by
            - sort(str): The sort order ('ASC' or 'DESC')
        :return: A list of model objects, for example [model(DataModel),...]
        """
        query_params["order_by"] = "value"
        return await BaseActions.get_all(
            AwardModelDB,
            query_params
        )

    @classmethod
    async def get_awards_where(cls, conditions: list, query_params: dict):
        """
        Get all awards from the database that match the specified conditions
        :param conditions(list): A list of conditions to match
        :param params(dict): A dictionary of query parameters
            - order_by(str): The field to sort by
            - sort(str): The sort order ('ASC' or 'DESC')
        :return: A list of model objects, for example [model(DataModel),...]
        """
        return await BaseActions.get_all_where(
            AwardModelDB,
            conditions,
            query_params
        )

    @classmethod
    async def get_award(cls, award_uuid: str):
        """
        Get one award from the database
        :param award_uuid(str): The uuid of the award to query
        :return: The award model(DataModel instance)
        """
        return await BaseActions.get_one_where(
            AwardModelDB,
            [AwardModelDB.uuid == award_uuid]
        )

    @classmethod
    async def get_upload_url(cls, award_uuid, file_name, upload_type):
        if upload_type == "image":
            return await UploadActions.generate_blueboard_upload_url(award_uuid, file_name)

        raise ExceptionHandling.custom400(f"Upload type {upload_type} is not supported")

    @classmethod
    async def create_award(cls, awards):
        """
        Create one or more awards in the database
        :param award_objs(AwardModel | list[AwardModel]): A list of Award models to create
        :return: The list of created award models
        """
        if isinstance(awards, list):
            to_create = []
            to_return = []
            for award in awards:
                award_model = await cls.to_award_model(award)
                existing = await cls.check_if_award_exists(
                        award_model.name,
                        False
                    )
                if existing:
                    to_return.append(existing)
                else:
                    to_create.append(award_model)
            if to_create:
                to_return.extend(await BaseActions.create(to_create))
            return to_return
        award_model = await cls.to_award_model(awards)
        existing = await cls.check_if_award_exists(
                award_model.name,
                False
            )
        if existing:
            return existing
        return await BaseActions.create(award_model)

    @staticmethod
    async def to_award_model(award):
        return AwardModelDB(
            **award.dict()
        )

    @classmethod
    async def update_award(cls, award_uuid: str, update_obj: AwardUpdate):
        """
        Update one award in the database
        :param award_uuid(str): The uuid of the award to update
        :param update_obj(AwardUpdate):The model object containing the updated fields
        :return: The updated award model
        """
        if update_obj.name:
            await cls.check_if_award_exists(update_obj.name)
        if update_obj.hero_image:
            update_obj.hero_image, _ = await UploadActions.verify_upload_file("image", update_obj.hero_image)
        return await BaseActions.update(
            AwardModelDB,
            [AwardModelDB.uuid == award_uuid],
            update_obj
        )

    @classmethod
    async def delete_award(cls, award_uuid: str):
        """
        Delete one award from the database
        :param award_uuid(str): The uuid of the award to delete
        :return: Status of deletion and the deleted model object
        """
        client_award = await BaseActions.check_if_one_exists(
            ClientAwardModelDB,
            [ClientAwardModelDB.award_uuid == award_uuid]
        )
        if client_award:
            return await ExceptionHandling.custom409(
                f"Cannot delete, award {award_uuid} is currently in use"
            )
        return await BaseActions.delete_one(
            AwardModelDB,
            [AwardModelDB.uuid == award_uuid]
        )

    @classmethod
    async def delete_all_where(cls, conditions: list):
        """
        Delete all awards from the database that match the specified conditions
        :param conditions(list): A list of conditions to filter by
        :return: Status of deletion and the deleted model object(s)
        """
        return await BaseActions.delete_all(
            AwardModelDB,
            conditions
        )
