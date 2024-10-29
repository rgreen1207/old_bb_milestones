import os
import random
from uuid import uuid4

from fastapi import HTTPException
from pydantic import BaseModel
from starlette import status

from app.actions.base_actions import BaseActions
from app.actions.users import UserActions
from app.actions.users.services import UserServiceActions
from app.libraries.sms import send_sms_worker
from app.libraries.sparkpost import send_auth_email
from app.models.clients import ClientUserModelDB
from app.models.users import UserServiceModelDB, UserServiceUpdate
from app.models.users.auth.auth_models import CreateAuthModel, AuthResponseModel, RedeemAuthModel
from cryptography.fernet import Fernet, InvalidToken

secretish_key = os.environ["FERNET_KEY"]
key = bytes(secretish_key,'UTF-8')
da_vinci = Fernet(key)


class ExpiredMessage(BaseModel):
    detail: str = "Expired Login Token"


class AuthActions(BaseActions):

    @classmethod
    async def post_auth_handler(cls, auth_model: CreateAuthModel):
        check_user_service = await cls.post_auth_creation(auth_model)
        if check_user_service:
            new_auth_response = AuthResponseModel(
                login_secret=check_user_service.login_secret,
                login_token=check_user_service.login_token,
                service_user_id=check_user_service.service_user_id,
                service_uuid=check_user_service.service_uuid
            )
            return new_auth_response

    @classmethod
    async def post_auth_creation(cls, auth_model):
        service = await cls.get_one_where(
            UserServiceModelDB,
            [
            UserServiceModelDB.service_uuid == auth_model.service_uuid,
            UserServiceModelDB.service_user_id == auth_model.service_user_id
            ]
        )

        auth_object = await cls.generate_auth(service)

        updates = UserServiceUpdate(
            login_token=auth_object.login_token,
            login_secret=auth_object.login_secret
        )


        response = await UserServiceActions.update_service(
            auth_object.user_uuid,
            auth_object.uuid,
            updates
        )

        return response

    @classmethod
    async def redeem_auth_handler(cls, redeem_auth_model):
        check_redeem = await cls.check_for_match_put(redeem_auth_model)
        if check_redeem:
            return await UserActions.get_user_by_uuid(check_redeem.user_uuid)
        else:
            return check_redeem

    @classmethod
    async def check_for_match_put(cls, redeem_auth_model: RedeemAuthModel):
        is_match = await cls.check_if_exists(
            UserServiceModelDB,
            [
                UserServiceModelDB.login_token == redeem_auth_model.login_token,
                UserServiceModelDB.login_secret == redeem_auth_model.login_secret
            ]
        )

        try:
            da_vinci.decrypt(redeem_auth_model.login_secret, ttl=900)
        except InvalidToken:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=ExpiredMessage().detail
            )

        if is_match:
            await cls.delete_token_secret(redeem_auth_model)
            return is_match
        else:
            return is_match

    @classmethod
    async def generate_auth(cls, service_obj):
        if service_obj.service_uuid == "email":
            service_obj.login_token = uuid4().hex
            service_obj.login_secret = da_vinci.encrypt(uuid4().bytes)

            sent_email = await cls.send_email_handler(service_obj)
            if sent_email:
                return service_obj
            else:
                print("error")
                return service_obj

        else:
            service_obj.login_token = str(random.randint(1000, 9999))
            service_obj.login_secret = da_vinci.encrypt(uuid4().bytes)

            sent_message = await cls.send_sms_handler(service_obj)
            if sent_message:
                return service_obj
            else:
                print("error")
                return service_obj

    @classmethod
    async def send_sms_handler(cls, service_obj_cell):
        sent_message = await send_sms_worker(service_obj_cell)
        if sent_message:
            return sent_message
        else:
            # NEED TO MAKE THIS ERROR HANDLING BETTER
            print("error sending text")
            return None

    @classmethod
    async def send_email_handler(cls, service_obj):
        response = await send_auth_email(service_obj)
        if response["total_accepted_recipients"] == 1:
            return response
        else:
            # NEED TO MAKE THIS ERROR HANDLING BETTER
            print("error sending text")
            return None

    @classmethod
    async def grab_admin_level(cls, user_object: dict):
        client_user = await cls.get_one_where(
            ClientUserModelDB,
            [
                ClientUserModelDB.user_uuid == user_object["uuid"]
            ]
        )
        return client_user.uuid

    @classmethod
    async def delete_token_secret(cls, redeem_auth_model):
        updates = UserServiceUpdate(
            login_token=uuid4().hex,
            login_secret=uuid4().hex
        )

        response = await cls.update(
            UserServiceModelDB,
            [
                UserServiceModelDB.login_token == redeem_auth_model.login_token,
                UserServiceModelDB.login_secret == redeem_auth_model.login_secret
            ],
            updates
        )
        return response

