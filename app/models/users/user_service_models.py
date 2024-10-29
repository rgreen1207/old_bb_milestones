from enum import Enum
from typing import Optional
from pydantic import Field
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base_class import Base, BasePydantic
from sqlalchemy.dialects import mysql
Integer = mysql.INTEGER


class ServiceID(str, Enum):
    email = "email"
    cell = "cell"
    slack = "slack"
    teams = "teams"
    web = "web"

    def __repr__(self) -> str:
        # return super().__repr__()
        return self.value


class UserServiceStatus(str, Enum):
    exists = "exists"
    created = "service created"
    updated = "service updated"


class UserServiceModelDB(Base):
    __tablename__ = "user_service"

    uuid: Mapped[str] = mapped_column(String(56), default=None, primary_key=True)
    user_uuid: Mapped[Optional[str]] = mapped_column(String(56), default=None, nullable=True)
    service_uuid: Mapped[Optional[str]] = mapped_column(String(56), default=None, nullable=True)
    service_user_id: Mapped[Optional[str]] = mapped_column(String(255), default=None, nullable=True)
    service_user_screenname: Mapped[Optional[str]] = mapped_column(String(255), default=None, nullable=True)
    service_user_name: Mapped[Optional[str]] = mapped_column(String(255), default=None, nullable=True)
    service_access_token: Mapped[Optional[str]] = mapped_column(String(255), default=None, nullable=True)
    service_access_secret: Mapped[Optional[str]] = mapped_column(String(255), default=None, nullable=True)
    service_refresh_token: Mapped[Optional[str]] = mapped_column(String(255), default=None, nullable=True)
    time_created: Mapped[Optional[int]] = mapped_column(Integer(11), default=None, nullable=True)
    time_updated: Mapped[Optional[int]] = mapped_column(Integer(11), default=None, nullable=True)
    login_secret: Mapped[Optional[str]] = mapped_column(String(255), default=None, nullable=True)
    login_token: Mapped[Optional[str]] = mapped_column(String(56), default=None, nullable=True)


class UserServiceModel(BasePydantic):
    uuid: Optional[str]
    user_uuid: Optional[str]
    service_uuid: Optional[str]
    service_user_id: Optional[str]
    service_user_screenname: Optional[str]
    service_user_name: Optional[str]
    service_access_token: Optional[str]
    service_access_secret: Optional[str]
    service_refresh_token: Optional[str]
    time_created: Optional[int]
    time_updated: Optional[int]
    login_secret: Optional[str]
    login_token: Optional[str]


class UserServiceResponse(UserServiceModel):
    pass


class ServiceListResponse(BasePydantic):
    email: Optional[list[UserServiceModel]]
    cell: Optional[list[UserServiceModel]]


class UserServiceCreate(BasePydantic):
    service_uuid: ServiceID
    service_user_id: str
    service_user_screenname: Optional[str]
    service_user_name: Optional[str]


class ServiceStatus(UserServiceModel):
    status: Optional[UserServiceStatus] = Field(
        default=None,
        description="This mapped_column can have the values 'exists' or 'admin created'."
    )


class UserServiceUpdate(BasePydantic):
    service_user_screenname: Optional[str]
    service_user_name: Optional[str]
    service_access_token: Optional[str]
    service_access_secret: Optional[str]
    service_refresh_token: Optional[str]
    login_secret: Optional[str]
    login_token: Optional[str]


class ServiceBulk(UserServiceUpdate):
    uuid: str


class ServiceDelete(BasePydantic):
    service_uuid: str
