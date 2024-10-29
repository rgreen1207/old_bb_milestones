from app.seed_data.seed_clients.client_models_seed import clients
#from app.seed_data.seed_clients.seed_client_awards import static_awards
from app.seed_data.seed_clients.seed_client_users import generate_client_users

async def generate_all_client_info():
    client_list = []
    client_list.extend(clients)
    #client_list.extend(await static_awards())

    return client_list

async def create_client_users():
    await generate_client_users(clients)