from typing import Optional
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.actions.utils import new_9char
from app.enums import AwardType, ChannelType
from app.models.base_class import Base, BasePydantic
from app.actions.base_actions import BaseActions
from app.models.award.award_models import AwardModelDB
from sqlalchemy.dialects import mysql
Integer = mysql.INTEGER

class ClientAwardModelDB(Base):
    __tablename__ = "client_award"

    uuid: Mapped[str] = mapped_column(String(65), default=None, primary_key=True, index=True)
    client_uuid: Mapped[str] = mapped_column(String(56), default=None, index=True, nullable=True)
    client_award_9char: Mapped[str] = mapped_column(String(9), default=None, index=None, nullable=True)
    award_uuid: Mapped[str] = mapped_column(String(56), default=0, nullable=True)
    name: Mapped[str] = mapped_column(String(255), default=None, nullable=True)
    description: Mapped[str] = mapped_column(Text, default=None, nullable=True)
    hero_image: Mapped[str] = mapped_column(String(4), default=None, nullable=True)
    time_created: Mapped[int] = mapped_column(Integer(11), default=None, nullable=True)
    time_updated: Mapped[int] = mapped_column(Integer(11), default=None, nullable=True)

    def __init__(self, **data):
        super().__init__(**data)
        if not self.client_award_9char:
            self.client_award_9char = new_9char()
        if not self.uuid:
            self.uuid = self.client_uuid + self.client_award_9char


class ClientAwardModel(BasePydantic):
    uuid: str
    client_uuid: Optional[str]
    client_award_9char: Optional[str]
    award_uuid: Optional[str]
    name: Optional[str]
    description: Optional[str]
    hero_image: Optional[str]
    time_created: Optional[int]
    time_updated: Optional[int]


class ClientAwardCreate(BasePydantic):
    award_uuid: Optional[str]
    name: Optional[str]
    description: Optional[str]
    hero_image: Optional[str]


class ClientAwardUpdate(BasePydantic):
    award_uuid: Optional[str]
    name: Optional[str]
    description: Optional[str]
    hero_image: Optional[str]


class ClientAwardResponse(ClientAwardModel):
    channel: Optional[ChannelType]
    award_type: Optional[AwardType]
    value: Optional[int]

    def __init__(self, **data):
        super().__init__(**data)
        award = BaseActions.get_one(
            AwardModelDB,
            [AwardModelDB.uuid == self.award_uuid]
        )
        if award:
            self.channel = award.channel
            self.award_type = award.award_type
            self.value = award.value


class ClientAwardDelete(BasePydantic):
    ok: bool
    Deleted: ClientAwardModel
