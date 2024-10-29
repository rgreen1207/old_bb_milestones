from typing import Optional
from pydantic import validator
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.enums import ClientStatus
from app.models.base_class import Base, BasePydantic
from sqlalchemy.dialects import mysql
Integer = mysql.INTEGER


class ClientModelDB(Base):
    __tablename__ = "client"

    uuid: Mapped[str] = mapped_column(String(56), default=None, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), default=None, index=True, nullable=True)
    url: Mapped[str] = mapped_column(String(255), default=None, index=True, nullable=True)
    description: Mapped[str] = mapped_column(Text, default=None, index=True, nullable=True)
    time_created: Mapped[int] = mapped_column(Integer(11), default=None, nullable=True)
    time_updated: Mapped[int] = mapped_column(Integer(11),default=None, nullable=True)
    time_ping: Mapped[int] = mapped_column(Integer(11), default=None, nullable=True)
    status: Mapped[int] = mapped_column(Integer(4), default=1, nullable=True)


class ClientModel(BasePydantic):
    uuid: Optional[str]
    name: Optional[str]
    url: Optional[str]
    description: Optional[str]
    time_created: Optional[int]
    time_updated: Optional[int]
    time_ping: Optional[int]
    status: Optional[ClientStatus]


class ClientResponse(ClientModel):
    pass


class ClientExpanded(ClientModel):
    budgets: dict


class ClientCreate(BasePydantic):
    name: str
    description: str
    status: Optional[ClientStatus]
    url: Optional[str]

    @validator('status', pre=False)
    def validate_award_type(cls, v, field):
        return field.type_[v].value


class ClientUpdate(BasePydantic):
    name: Optional[str]
    description: Optional[str]
    status: Optional[ClientStatus]

    @validator('status', pre=False)
    def validate_award_type(cls, v, field):
        return field.type_[v].value


class ClientDelete(BasePydantic):
    ok: bool
    Deleted: ClientModel
