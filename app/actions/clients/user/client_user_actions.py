from app.actions.utils import convert_date_to_int
from app.actions.base_actions import BaseActions
from app.actions.helper_actions import HelperActions
from app.actions.users import UserActions
from app.models.clients import ClientUserModelDB, ClientUserExpand
from app.models.users import UserModelDB, UserServiceModelDB
from app.exceptions import ExceptionHandling
from app.utilities import SHA224Hash

class ClientUserActions:

    @staticmethod
    async def get_client_user_by_user_uuid(client_uuid: str, user_uuid: str):
        return await BaseActions.check_if_exists(
            ClientUserModelDB,
            [
                ClientUserModelDB.client_uuid == client_uuid,
                ClientUserModelDB.user_uuid == user_uuid
            ]
        )

    @staticmethod
    async def expand_client_user(client_user, user):
        client_user_expanded = ClientUserExpand.from_orm(client_user)
        client_user_expanded.user = user
        return client_user_expanded

    @classmethod
    async def create_client_user(cls, data: dict, path_params: dict, expand: bool = True):
        service_id = ["work_email", "personal_email", "cell_phone", "email_address"]
        user_objs = []
        client_user_objs = []
        for service in service_id:
            service_value = data.get(service)
            if service_value:
                response_obj = await cls.handle_user_and_service(data, path_params, expand, service)
                if type(response_obj) is UserModelDB:
                    user_objs.append(response_obj)
                elif type(response_obj) in (ClientUserModelDB, ClientUserExpand):
                    client_user_objs.append(response_obj)
        if not (user_objs or client_user_objs):
            raise ValueError("No user or client user objects returned")

        user_uuids = [user.uuid for user in user_objs if user is not None]
        if len(set(user_uuids)) > 1:
            raise ValueError("Multiple user objects returned for different service IDs")

        client_user_uuids = [client_user.uuid for client_user in client_user_objs if client_user is not None]
        if len(set(client_user_uuids)) > 1:
            raise ValueError("Multiple client user objects returned for different service IDs")

        user_obj = user_objs[0] if user_objs else None
        client_user_obj = client_user_objs[0] if client_user_objs else None

        client_user = await cls.add_new_client_user(
            data, path_params, user_obj
        ) if not client_user_obj else client_user_obj
        return client_user

    @classmethod
    async def handle_user_and_service(cls, data: dict, path_params, expand, service_id=None):
        user = None
        user_uuid = data.get("user_uuid")
        service = data.get(service_id)
        if not (user_uuid or service):
            return await ExceptionHandling.custom500(
                "Not enough information to create a new Client User. Please include either email address or the user_uuid."
            )
        if user_uuid:
            user = await BaseActions.check_if_exists(
                UserModelDB,
                [
                    UserModelDB.uuid == data["user_uuid"]
                ])
        elif service:
            user = await BaseActions.check_if_exists(
                UserModelDB,
                [
                    UserServiceModelDB.service_user_id == service,
                    UserModelDB.uuid == UserServiceModelDB.user_uuid,
                    UserModelDB.first_name == data.get("first_name"),
                    UserModelDB.last_name == data.get("last_name")
                ])

        if user:
            uuid = user.uuid
            client_user = await cls.get_client_user_by_user_uuid(path_params["client_uuid"], uuid)
            if client_user:
                if expand:
                    return await cls.expand_client_user(client_user, user)
                return client_user

        if not user and service:
            admin = data.get("admin", 0)
            if admin not in [0, 1, 2]:
                await ExceptionHandling.custom409("Invalid value for admin field, must be 0 or 1.")
            user = await UserActions.create_user_and_service(data, service_id)

        if not (user or service):
            return await ExceptionHandling.custom409(
                "Not enough information to create a new Client User, User, and Service User."
            )

        return user

    @classmethod
    async def add_new_client_user(cls, data: dict, path_params: dict, user, expand: bool = False):
        # Check if client user already exists
        client_user = await cls.get_client_user_by_user_uuid(user.uuid, user.uuid)

        if not client_user:
            client_user_obj = ClientUserModelDB(
                uuid=SHA224Hash(),
                user_uuid=user.uuid,
                client_uuid=path_params.get("client_uuid"),
                manager_uuid=await HelperActions.get_manager_uuid(data),
                employee_id=await HelperActions.get_employee_id(data),
                title=await HelperActions.get_title(data),
                department=await HelperActions.get_department(data),
                active=await HelperActions.get_active(data) if "active" in data.keys() else 1,
                time_hire=convert_date_to_int(data.get('time_hire')),
                time_start=convert_date_to_int(data.get('time_start')),
                admin=await HelperActions.get_admin(data),
            )

            client_user = await BaseActions.create(client_user_obj)
        return await cls.expand_client_user(client_user, user)

    @classmethod
    async def getExpandedClientUsers(cls, data, client_uuid, expansion):
        pass

    @staticmethod
    async def get_all_users(client_uuid: str, query_params: dict):
        return await BaseActions.get_all_where(
            ClientUserModelDB,
            [
                ClientUserModelDB.client_uuid == client_uuid
            ],
            query_params
        )

    @staticmethod
    async def get_user(path_params):
        return await BaseActions.get_one_where(
            ClientUserModelDB,
            [
                ClientUserModelDB.client_uuid == path_params["client_uuid"],
                ClientUserModelDB.user_uuid == path_params["user_uuid"]
            ]
        )

    @staticmethod
    async def update_user(path_params: dict, user_updates):
        return await BaseActions.update(
            ClientUserModelDB,
            [
                ClientUserModelDB.client_uuid == path_params["client_uuid"],
                ClientUserModelDB.uuid == path_params["user_uuid"]
            ],
            user_updates
        )

    @staticmethod
    async def update_users(path_params, user_updates):
        uuid_list = []
        for user in user_updates:
            if user.uuid:
                uuid_list.append(user.uuid)
            else:
                return await ExceptionHandling.custom400(f"Missing uuid in user update list for: {user}")
        return await BaseActions.bulk_update(
            ClientUserModelDB,
            [
                ClientUserModelDB.client_uuid == path_params.get("client_uuid"),
            ],
            user_updates,
            uuid_list
        )

    @staticmethod
    async def update_admin_client_user(path_params: dict, user_updates):
        if path_params.get("client_uuid") is None:
            conditions = [ClientUserModelDB.user_uuid == path_params['user_uuid']]
        else:
            conditions = [
                ClientUserModelDB.client_uuid == path_params['client_uuid'],
                ClientUserModelDB.user_uuid == path_params['user_uuid']
            ]

        return await BaseActions.update(
            ClientUserModelDB,
            conditions,
            user_updates
        )

    @staticmethod
    async def delete_user(path_params):
        return await BaseActions.delete_one(
            ClientUserModelDB,
            [
                ClientUserModelDB.client_uuid == path_params["client_uuid"],
                ClientUserModelDB.uuid == path_params["user_uuid"]
            ]
        )
