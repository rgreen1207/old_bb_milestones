from time import time
from app.actions.utils import convert_date_to_int
from app.actions.base_actions import BaseActions
from app.actions.helper_actions import HelperActions
from app.actions.users.services import UserServiceActions
from app.models.users import UserModelDB, UserServiceModelDB, UserExpanded

class UserActions:

    @classmethod
    async def get_user_by_uuid(cls, uuid):
        return await BaseActions.get_one_where(UserModelDB, [UserModelDB.uuid == uuid])

    @classmethod
    async def get_user_by_service_id(cls, user_uuid, service_id):
        return await BaseActions.check_if_exists(
            UserModelDB,
            [
                UserServiceModelDB.service_user_id == service_id,
                UserServiceModelDB.user_uuid == user_uuid,
                UserServiceModelDB.user_uuid == UserModelDB.uuid

            ]
        )

    @classmethod
    async def get_user_by_name(cls, first_name, last_name, service_id=None):
        return await BaseActions.check_if_exists(
            UserModelDB,
            [
                UserModelDB.first_name == first_name,
                UserModelDB.last_name == last_name#,
                # UserServiceModelDB.service_user_id == service_id,
            ]
        )

    @classmethod
    async def get_all_users(cls, query_params: dict):
        return await BaseActions.get_all(UserModelDB, query_params)

    @classmethod
    async def get_user(cls, user_uuid, expand_services=False):
        user = await cls.get_user_by_uuid(user_uuid)
        if expand_services:
            return await cls.expand_services(user)
        return user

    @staticmethod
    async def expand_services(user_obj, service=None):
        user_expand = UserExpanded.from_orm(user_obj)
        if service:
            user_expand.services = service
        else:
            user_expand.services = await UserServiceActions.get_all_services(user_obj.uuid)
        return user_expand

    @staticmethod
    async def get_service_id(new_user_obj: dict, service_id=None):
        """Get the service ID from the specified user object
        :param new_user_obj: The user object to get the service ID from
        :return: A namedtuple containing the service type and service ID, or None if it couldn't be found
        """
        if (service_id := await HelperActions.get_email_from_header(new_user_obj, service_id)):
            return service_id
        elif (service_id := await HelperActions.get_cell_from_header(new_user_obj, service_id)):
            return service_id
        else:
            return None

    @classmethod
    async def create_user(cls, users, expand_services):
        if isinstance(users, list):
            for i, user_obj in enumerate(users):
                users[i] = await cls.create_user_and_service(user_obj)
                if expand_services:
                    users[i] = await cls.expand_services(users[i])
        else:
            users = await cls.create_user_and_service(users)
            if expand_services:
                users = await cls.expand_services(users)

        return users

    @classmethod
    async def create_user_and_service(cls, new_user_data, service=None):
        if hasattr(new_user_data, "dict"):
            new_user_data: dict = new_user_data.dict(exclude_none=True)
        service_id = await cls.get_service_id(new_user_data, service)
        if not service_id:
            raise Exception("service_id required")
        first_name = await HelperActions.get_fname_from_header(new_user_data)
        last_name = await HelperActions.get_lname_from_header(new_user_data)
        birthday = convert_date_to_int(new_user_data.get('time_birthday'))

        user = await cls.get_user_by_name(new_user_data["first_name"], new_user_data["last_name"])

        if user:
            # TODO: change to "status = exists" class format
            service_user = await cls.get_user_by_service_id(user.uuid, service_id.value)
            if service_user:
                return service_user
            else:
                new_service = await UserServiceActions.create_service_for_new_user(user, service_id)
                if not new_service:
                    raise Exception("Service Creation Failed")
                return user

        # TODO: turn back on when Nominatim server is working
        # lat, lon = await utils.get_location_coord(new_user_data.get("location"))
        lat, lon = None, None

        new_user_obj = UserModelDB(
            first_name = first_name,
            last_name= last_name,
            latitude = lat,
            longitude = lon,
            time_ping = int(time()),
            admin = await HelperActions.get_admin(new_user_data),
            time_birthday = birthday
        )
        user_db = await BaseActions.create(new_user_obj)
        new_service = await UserServiceActions.create_service_for_new_user(user_db, service_id)
        if not new_service:
            raise Exception("Service Creation Failed")
        return user_db

    @classmethod
    async def update_user(cls, user_uuid, updates):
        return await BaseActions.update(UserModelDB, [UserModelDB.uuid == user_uuid], updates)

    @classmethod
    async def delete_user(cls, user_uuid):
        return await BaseActions.delete_one(UserModelDB, [UserModelDB.uuid == user_uuid])

    @classmethod
    async def delete_test_user(cls, user_uuid):
        services = await UserServiceActions.get_all_services(user_uuid)
        for key, value in services.items():
            for item in value:
                await BaseActions.delete_one(UserServiceModelDB, [UserServiceModelDB.uuid == item.uuid])
