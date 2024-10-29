
from typing import Optional
from app.models.base_class import BasePydantic


class CreateAuthModel(BasePydantic):
    service_uuid: Optional[str] = None
    service_user_id: Optional[str] = None


class RedeemAuthModel(BasePydantic):
    login_secret: Optional[str] = None
    login_token: Optional[str] = None


class AuthResponseModel(BasePydantic):
    login_secret: Optional[str] = None
    login_token: Optional[str] = None
    service_uuid: Optional[str] = None
    service_user_id: Optional[str] = None
