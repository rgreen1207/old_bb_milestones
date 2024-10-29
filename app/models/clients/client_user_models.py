from typing import Optional
from pydantic import validator
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.enums import Admin
from app.models.base_class import Base, BasePydantic
from app.models.users import UserModel
from sqlalchemy.dialects import mysql
Integer = mysql.INTEGER


class ClientUserModelDB(Base):
    __tablename__ = "client_user"

    uuid: Mapped[str] = mapped_column(String(56), default=None, primary_key=True, index=True)
    user_uuid: Mapped[str] = mapped_column(String(56), default=None, index=True, nullable=True)
    client_uuid: Mapped[str] = mapped_column(String(56), default=None, index=True, nullable=True)
    manager_uuid: Mapped[str] = mapped_column(String(56), default=None, index=True, nullable=True)
    employee_id: Mapped[str] = mapped_column(String(255), default=None, index=True, nullable=True)
    title: Mapped[str] = mapped_column(String(255), default=None, nullable=True)
    department: Mapped[str] = mapped_column(String(255), default=None, nullable=True)
    active: Mapped[bool] = mapped_column(default=None, nullable=True)
    time_created: Mapped[int] = mapped_column(Integer(11), default=None, nullable=True)
    time_updated: Mapped[int] = mapped_column(Integer(11), default=None, nullable=True)
    time_hire: Mapped[int] = mapped_column(Integer(11), default=None, nullable=True)
    time_start: Mapped[int] = mapped_column(Integer(11), default=None, nullable=True)
    admin: Mapped[int] = mapped_column(Integer(11), default=None, nullable=True)


class ClientUserModel(BasePydantic):
    uuid: Optional[str]
    user_uuid: Optional[str]
    client_uuid: Optional[str]
    manager_uuid: Optional[str]
    employee_id: Optional[str]
    title: Optional[str]
    department: Optional[str]
    active: Optional[bool]
    time_created: Optional[int]
    time_updated: Optional[int]
    time_hire: Optional[int]
    time_start: Optional[int]
    admin: Optional[Admin]


class ClientUserResponse(ClientUserModel):
    pass


class ClientUserCreate(BasePydantic):
    # user level fields
    first_name: Optional[str]
    last_name: Optional[str]
    location: Optional[str]
    time_birthday: Optional[int]
    # service level fields
    service_uuid: Optional[str] # "email" or "cell"
    service_user_id: Optional[str] # email address or cell phone number
    #include title, manager_uuid, department, active, admin
    admin: Optional[Admin]

    @validator('admin', pre=False)
    def validate_award_type(cls, v, field):
        return field.type_[v].value


class ClientUserUpdate(BasePydantic):
    uuid: Optional[str]
    manager_uuid: Optional[str]
    employee_id: Optional[str]
    title: Optional[str]
    department: Optional[str]
    active: Optional[bool]
    admin: Optional[Admin]

    @validator('admin', pre=False)
    def validate_award_type(cls, v, field):
        return field.type_[v].value


class ClientUserExpand(ClientUserModel):
    user: Optional[UserModel]
    # user_service: Optional[dict]


class ClientUserDelete(BasePydantic):
    ok: bool
    Deleted: ClientUserModel
