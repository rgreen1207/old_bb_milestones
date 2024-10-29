import os

from app.models.users import UserServiceModelDB
from app.models.messages import MessageModel
from app.actions.messages.templates.template_actions import MessageTemplateActions
from sparkpost import SparkPost

from app.models.users.user_models import UserModel
_scriptname = "ThirdParty.SparkPost"


SPARKPOST_KEY = os.environ["SPARKPOST_KEY"]
sp = SparkPost(SPARKPOST_KEY)

BASE_URL = os.getenv("BASE_URL", "https://milestones.blueboard.app/")
REDEEM_URL = f"{BASE_URL}auth/verify-email-token?token="

async def send_auth_email(user_service: UserServiceModelDB):

    response = sp.transmissions.send(
        use_sandbox=False,
        recipients=[user_service.service_user_id],
        html=await MessageTemplateActions.create_auth_email(REDEEM_URL + user_service.login_token),
        from_email="no-reply@mail.blueboard.app",
        subject="Blueboard Login Token"
    )

    return response

async def send_message_email(message_details: dict, recipient: UserModel, recipient_email: str):
    response = sp.transmissions.send(
        use_sandbox=False,
        recipients=[recipient_email],
        html=await get_email_body(message_details, recipient),
        from_email="no-reply@mail.blueboard.app",
        subject="Blueboard Message",
    )

    return response

async def get_email_body(message: MessageModel, recipient: str,):
    return await {
        1: MessageTemplateActions.create_welcome_email,
        2: MessageTemplateActions.create_auth_email,
        3: MessageTemplateActions.create_award_email,
        4: MessageTemplateActions.create_anniversary_email,
        5: MessageTemplateActions.create_birthday_email,
        # 6: MessageTemplateActions.create_redeem_email,
        # 7: MessageTemplateActions.create_message_email,
        # 8: MessageTemplateActions.create_reminder_email,
        # 9: MessageTemplateActions.create_survey_email
    }[message['message'].message_type](message, recipient)
