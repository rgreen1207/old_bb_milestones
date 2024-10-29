from app.seed_data.seed_messages.seed_system_emails import system_emails
from app.seed_data.seed_messages.seed_system_sms import system_sms

async def generate_all_message_info():
    message_list = []
    message_list.extend(system_emails)
    message_list.extend(system_sms)
    return message_list