from app.libraries.sparkpost import send_message_email
from app.libraries.sms import send_message_text
from app.models.messages import MessageSend

class MessageSendingHandler:

    channel_types = {
                1: "email",
                2: "cell",
                # 4: "p2p_slack",
                # 8: "p2p_teams",
                # 16: "web"
            }

    @classmethod
    async def send_message(cls, message_details: dict):
        response = []
        message = message_details['message']
        for recipient in message_details['recipients']:
            response.append(
                    await {
                        1: send_message_email,
                        2: send_message_text,
                        #4: await send_slack_message(message, recipients),
                        #8: await send_ms_teams_message(message, recipients),
                        #16: await send_web_message(message, recipients)
                }[message.channel](
                    message_details,
                    recipient,
                    await cls.get_service_user_id(message.channel, recipient))
                )
        return response

    @classmethod
    async def get_service_user_id(cls, message_channel: int, recipient: MessageSend):
        return recipient['user'].services[cls.channel_types[message_channel]][0].service_user_id
