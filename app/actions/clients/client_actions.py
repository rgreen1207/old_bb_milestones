from app.actions.base_actions import BaseActions
from app.models.clients import ClientModelDB, ClientUpdate
from app.models.programs.program_event_models import ProgramEventModelDB
from app.exceptions import ExceptionHandling

class ClientActions:

    @staticmethod
    async def get_all_clients(query_params: dict):
        return await BaseActions.get_all(ClientModelDB, query_params)

    @staticmethod
    async def get_client(client_uuid: str):
        return await BaseActions.get_one_where(
            ClientModelDB,
            [ClientModelDB.uuid == client_uuid]
        )

    @staticmethod
    async def get_client_name(client_uuid: str):
        return await BaseActions.get_one_where(
            ClientModelDB.name,
            [ClientModelDB.uuid == client_uuid]
        )

    @staticmethod
    async def check_if_client_exists_by_name(client_name: str, error=True):
        client = await BaseActions.check_if_exists(
            ClientModelDB,
            [ClientModelDB.name == client_name]
        )
        if client and error:
            return await ExceptionHandling.custom405(f"Client with name '{client.name}' already exists.")
        elif client and not error:
            return client
        else:
            return None

    @staticmethod
    async def to_client_db_model(client_data):
        return ClientModelDB(
            name=client_data.name,
            description=client_data.description,
            status=client_data.status,
            url=client_data.url
        )

    @classmethod
    async def create_client(cls, client_data):
        if isinstance(client_data, list):
            to_create = []
            return_list = []
            for client in client_data:
                existing_client = await cls.check_if_client_exists_by_name(client.name, False)
                if existing_client:
                    return_list.append(existing_client)
                else:
                    to_create.append(await cls.to_client_db_model(client))
            if to_create:
                return_list.extend(await BaseActions.create(to_create))
            return return_list
        client = await cls.check_if_client_exists_by_name(client_data.name, False)
        if client:
            return client
        return await BaseActions.create(await cls.to_client_db_model(client_data))

    @classmethod
    async def update_client(cls, client_uuid: str, update_obj: ClientUpdate):
        if update_obj.name:
            await cls.check_if_client_exists_by_name(update_obj.name)
        return await BaseActions.update(
            ClientModelDB,
            [ClientModelDB.uuid ==client_uuid],
            update_obj
        )

    @staticmethod
    async def delete_client(client_uuid: str):
        client = await BaseActions.get_one_where(ClientModelDB, [ClientModelDB.uuid == client_uuid])
        if client.status == 1:
            return await ExceptionHandling.custom400(f"Client '{client.name}' is currently active. Please deactivate before deleting.")
        return await BaseActions.delete_one(
            ClientModelDB,
            [ClientModelDB.uuid == client_uuid]
        )

    # These is for postman and pytest purposes only. Only accesible in those enviornments.
    @staticmethod
    async def delete_all_client_events(client_uuid: str):
        return await BaseActions.delete_all(
            ProgramEventModelDB,
            [
                ProgramEventModelDB.client_uuid == client_uuid
            ]
        )


    # this is only being used for postman/pytests through various checks
    @staticmethod
    async def delete_all_test_message_events(program_9char: str):
        return await BaseActions.delete_all(
            ProgramEventModelDB,
            [
                ProgramEventModelDB.program_9char == program_9char
            ]
        )
