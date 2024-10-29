from string import Template
from jinja2 import Environment, FileSystemLoader

templateLoader = FileSystemLoader(searchpath="app/templates/system_templates")
templateEnv = Environment(loader=templateLoader)


class MessageTemplateActions:

    @classmethod
    async def create_award_email(cls, message_details, recipient):
        return templateEnv.get_template("award.html").render(
            RECIPIENT_FIRST_NAME= await cls.get_recipient_first_name(recipient),
            COMPANY_NAME= await cls.get_recipient_company_name(message_details),
            AWARD_LEVEL= await cls.get_award_level(recipient),
        )

    @classmethod
    async def create_anniversary_email(cls, message_details, recipient):
        return templateEnv.get_template("anniversary.html").render(
            RECIPIENT_FIRST_NAME= await cls.get_recipient_first_name(recipient),
            ANNIVERSARY= await cls.get_recipient_anniv(recipient),
            COMPANY_NAME= await cls.get_recipient_company_name(message_details),
            AWARD_LEVEL= await cls.get_award_level(recipient),
        )

    @classmethod
    async def create_birthday_email(cls, message_details, recipient):
        return templateEnv.get_template("birthday.html").render(
            RECIPIENT_FIRST_NAME= await cls.get_recipient_first_name(recipient),
            COMPANY_NAME= await cls.get_recipient_company_name(message_details),
            AWARD_LEVEL= await cls.get_award_level(recipient),
        )

    @classmethod
    async def create_welcome_email(cls, message_details, recipient):
        return templateEnv.get_template("welcome.html").render(
            COMPANY_NAME= await cls.get_recipient_company_name(message_details),
        )

    @classmethod
    async def create_anniversary_text(cls, message_details, recipient):
        return Template(message_details['message'].body).safe_substitute(
            fname= await cls.get_recipient_first_name(recipient),
            anniv= await cls.get_recipient_anniv(recipient),
            company= await cls.get_recipient_company_name(message_details),
            award= await cls.get_award_level(recipient)
        )

    @classmethod
    async def create_birthday_text(cls, message_details, recipient):
        return Template(message_details['message'].body).safe_substitute(
            fname= await cls.get_recipient_first_name(recipient),
            company= await cls.get_recipient_company_name(message_details),
            award= await cls.get_award_level(recipient)
        )

    @staticmethod
    async def create_auth_email(auth_url):
        return templateEnv.get_template("auth.html").render(
            AUTH_URL = auth_url
        )

    @staticmethod
    async def get_recipient_first_name(recipient):
        return recipient['user'].first_name

    @staticmethod
    async def get_recipient_last_name(recipient):
        return recipient['user'].last_name

    @staticmethod
    async def get_recipient_anniv(recipient):
        return recipient['anniversary']

    @staticmethod
    async def get_recipient_company_name(message_details):
        return message_details['client'].name

    @staticmethod
    async def get_award_level(recipient):
        return recipient['award'].name
