from app.actions.base_actions import BaseActions
from app.seed_data.seed_clients import generate_all_client_info, create_client_users
from app.seed_data.seed_messages import generate_all_message_info
from app.seed_data.seed_system_awards import system_awards

async def seed_database():
    seed_list = []
    seed_list.extend(await generate_all_client_info())
    seed_list.extend(await system_awards())
    seed_list.extend(await generate_all_message_info())
    await BaseActions.seed_database(seed_list)

    await create_client_users() #does not create a list to return. instead creates all db items in runtime