from typing import Optional
from collections import namedtuple
from app.models.users import UserModelDB, UserServiceModelDB, UserServiceUpdate, UserServiceCreate, ServiceStatus
from app.actions.helper_actions import HelperActions
from app.actions.base_actions import BaseActions

class UserServiceActions(BaseActions):

    @classmethod
    async def check_existing(cls, service:UserServiceCreate):
        id = service.service_user_id

        service_obj = await cls.check_if_exists(
            UserServiceModelDB,
            [
            UserServiceModelDB.service_user_id == id,
            UserServiceModelDB.user_uuid == UserModelDB.uuid
            ]
        )

        if service_obj:
            existing_service = ServiceStatus.from_orm(service_obj)
            existing_service.status = "exists"
            return existing_service
        return service

    @classmethod
    async def create_service_for_new_user(cls, user_obj, service_id: namedtuple):

        new_user_service = UserServiceModelDB(
            user_uuid = user_obj.uuid,
            service_uuid = service_id.type,
            service_user_id = service_id.value,
            service_user_screenname = f"{user_obj.first_name} {user_obj.last_name}",
            service_user_name = await HelperActions.make_username(user_obj.first_name, user_obj.last_name),
            service_access_token = "access token",
            service_access_secret = "secret token",
            service_refresh_token = "refresh token",
            login_token="place_holder",
            login_secret="place_holder"
        )
        return await cls.create(new_user_service)

    @classmethod
    async def get_service(cls, user_uuid: str, service_uuid: str):
        return await cls.get_one_where(
            UserServiceModelDB,
            [
                UserServiceModelDB.user_uuid == user_uuid,
                UserServiceModelDB.uuid == service_uuid
            ]
        )

    @classmethod
    async def get_all_services(cls, user_uuid: str, query_params: Optional[dict] = None):
        services = await cls.get_all_where(
            UserServiceModelDB,
            [UserServiceModelDB.user_uuid == user_uuid],
            query_params,
            pagination=False
        )

        result = {}
        for service in services:
            key = service.service_uuid
            if key not in result:
                result[key] = []
            result[key].append(service)
        return result

    @classmethod
    async def create_user_service(cls, user_uuid: str, service_obj):
        if isinstance(service_obj, ServiceStatus):
            return service_obj

        service_obj = UserServiceModelDB(
            user_uuid = user_uuid,
            service_uuid = service_obj.service_uuid,
            service_user_id = service_obj.service_user_id
        )
        service = await cls.create(service_obj)
        new_service = ServiceStatus.from_orm(service)
        new_service.status = "service created"
        return new_service

    @classmethod
    async def update_service(
        cls,
        user_uuid: str,
        service_uuid: str,
        updates: UserServiceUpdate
    ):
        return await cls.update(
            UserServiceModelDB,
            [
            UserServiceModelDB.user_uuid == user_uuid,
            UserServiceModelDB.uuid == service_uuid
            ],
            updates
        )

    @classmethod
    async def bulk_update_services(cls, user_uuid: str, updates: list):
        update_list = []
        for update in updates:
            db_update = UserServiceUpdate.from_orm(update)
            update_list.append(
                await cls.update_service(user_uuid, update.uuid, db_update)
            )
        return update_list

    @classmethod
    async def delete_service(cls, service_uuid: str):
        return await cls.delete_one(
            UserServiceModelDB,
            [UserServiceModelDB.uuid == service_uuid]
        )

    @classmethod
    async def bulk_delete_services(cls, service_delete: list):
        deleted_services = []
        for service in service_delete:
            deleted_services.append(
                await cls.delete_one(
                    UserServiceModelDB,
                    [UserServiceModelDB.uuid == service.service_uuid]
                )
            )
        return deleted_services
