from time import time
from typing import Union
from app.actions.base_actions import BaseActions
from app.utilities import SHA224Hash
from app.models.programs import AdminModelDB, AdminUpdate, AdminCreate, AdminStatus
from app.routers.v1.dependencies import verify_client_user

class ProgramAdminActions:

    @staticmethod
    async def get_program_admins(path_params, query_params):
        return await BaseActions.get_all_where(
            AdminModelDB,
            [
                AdminModelDB.client_uuid == path_params["client_uuid"],
                AdminModelDB.program_9char == path_params["program_9char"]
            ],
            query_params
        )

    @staticmethod
    async def get_program_admin(path_params):
        return await BaseActions.get_one_where(
            AdminModelDB,
            [
                AdminModelDB.user_uuid == path_params["user_uuid"],
                AdminModelDB.client_uuid == path_params["client_uuid"],
                AdminModelDB.program_9char == path_params["program_9char"]
            ]
        )

    @staticmethod
    async def create_program_admin(path_params: dict, admin_obj: AdminCreate):
        # verify provided user_uuid is related to the client
        await verify_client_user(admin_obj.user_uuid, path_params["client_uuid"])
        current_time = int(time())

        admin = AdminModelDB(
            uuid = SHA224Hash(f"{admin_obj.program_uuid}+{admin_obj.user_uuid}"),
            program_uuid=admin_obj.program_uuid,
            client_uuid=path_params["client_uuid"],
            program_9char=path_params["program_9char"],
            user_uuid=admin_obj.user_uuid,
            permissions=admin_obj.permissions if admin_obj.permissions else 1,
            time_created=current_time,
            time_updated=current_time
        )
        admin = await BaseActions.create(admin)
        new_admin = AdminStatus.from_orm(admin)
        new_admin.status = "admin created"
        return new_admin

    @classmethod
    async def create_program_admins(cls, path_params: dict, admin_obj: Union[AdminCreate, list]):
        if isinstance(admin_obj, list):
            for i, admin in enumerate(admin_obj):
                if isinstance(admin, AdminCreate):
                    admin_obj[i] = await cls.create_program_admin(path_params, admin)
            return admin_obj
        elif isinstance(admin_obj, AdminStatus):
            return admin_obj
        return await cls.create_program_admin(path_params, admin_obj)

    @staticmethod
    async def update_program_admin(path_params: dict, updates: AdminUpdate):
        return await BaseActions.update(
            AdminModelDB,
            [
                AdminModelDB.user_uuid == path_params["user_uuid"],
                AdminModelDB.client_uuid == path_params["client_uuid"],
                AdminModelDB.program_9char == path_params["program_9char"]
            ],
            updates
        )

    @staticmethod
    async def delete_program_admin(path_params: dict):
        return await BaseActions.delete_one(
            AdminModelDB,
            [
                AdminModelDB.user_uuid == path_params["user_uuid"],
                AdminModelDB.client_uuid == path_params["client_uuid"],
                AdminModelDB.program_9char == path_params["program_9char"]
            ]
        )

    @classmethod
    async def get_program_admin_by_user_id(cls, user_uuid, program_9char):
        return await BaseActions.check_if_exists(
            AdminModelDB,
            [
                AdminModelDB.user_uuid == user_uuid,
                AdminModelDB.program_9char == program_9char
            ]
        )

    @classmethod
    async def get_program_id(cls, program_9char):
        return await BaseActions.check_if_exists(
            AdminModelDB,
            [
                AdminModelDB.program_9char == program_9char
            ])

    @staticmethod
    async def check_existing(users: Union[AdminCreate, list[AdminCreate]], program_9char: str):
        if isinstance(users, list):
            for i, user in enumerate(users):
                admin = await ProgramAdminActions.get_program_admin_by_user_id(user.user_uuid, program_9char)
                if admin:
                    user = AdminStatus.from_orm(admin)
                    user.status = "existing admin"
                    users[i] = user
            return users
        admin = await ProgramAdminActions.get_program_admin_by_user_id(users.user_uuid, program_9char)
        if admin:
            admin = AdminStatus.from_orm(admin)
            admin.status = "existing admin"
            return admin
        return users
