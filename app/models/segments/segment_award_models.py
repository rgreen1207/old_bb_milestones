from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from sqlalchemy import String, Text
from app.models.base_class import Base, BasePydantic
from app.actions.base_actions import BaseActions
from app.actions.utils import new_9char
from app.models.clients.client_award_models import ClientAwardModelDB, ClientAwardResponse
from sqlalchemy.dialects import mysql
Integer = mysql.INTEGER


class SegmentAwardModelDB(Base):
    __tablename__ = "program_segment_award"

    uuid: Mapped[str] = mapped_column(String(83), default=None, primary_key=True)
    program_9char: Mapped[str] = mapped_column(String(9), default=None, nullable=True)
    program_award_9char: Mapped[str] = mapped_column(String(9), default=None, nullable=True)
    segment_9char: Mapped[str] = mapped_column(String(9), default=None, nullable=True)
    segment_award_9char: Mapped[str] = mapped_column(String(9), default=None, nullable=True)
    client_award_9char: Mapped[str] = mapped_column(String(9), default=None, nullable=True)
    client_uuid: Mapped[str] = mapped_column(String(56), default=None, nullable=True)
    name: Mapped[str] = mapped_column(String(255), default=None, nullable=True)
    description: Mapped[str] = mapped_column(Text, default=None, nullable=True)
    hero_image: Mapped[str] = mapped_column(String(4), default=None, nullable=True)
    time_created: Mapped[int] = mapped_column(Integer(11), default=None, nullable=True)
    time_updated: Mapped[int] = mapped_column(Integer(11), default=None, nullable=True)

    def __init__(self, **data):
        super().__init__(**data)
        if not self.segment_award_9char:
            self.segment_award_9char = new_9char()
        if not self.uuid:
            self.uuid = (self.client_uuid + self.program_9char + self.segment_9char + self.client_award_9char)


class SegmentAwardModel(BasePydantic):
    uuid: Optional[str]
    client_uuid: Optional[str]
    program_9char: Optional[str]
    program_award_9char: Optional[str]
    segment_9char: Optional[str]
    segment_award_9char: Optional[str]
    client_award_9char: Optional[str]
    name: Optional[str]
    description: Optional[str]
    hero_image: Optional[str]
    time_created: Optional[int]
    time_updated: Optional[int]


class SegmentAwardUpdate(BasePydantic):
    name: Optional[str]
    description: Optional[str]
    hero_image: Optional[str]


class SegmentAwardCreate(BasePydantic):
    client_award_9char: Optional[str]
    name: Optional[str]
    description: Optional[str]
    hero_image: Optional[str]


class SegmentAwardResponse(SegmentAwardModel):
    channel: Optional[int|str]
    award_type: Optional[int|str]
    value: Optional[int]

    def __init__(self, **data):
        super().__init__(**data)

        client_award = BaseActions.get_one(
            ClientAwardModelDB,
            [ClientAwardModelDB.client_award_9char == self.client_award_9char]
        )
        client_award = ClientAwardResponse(**client_award.to_dict())

        self.channel = client_award.channel
        self.award_type = client_award.award_type
        self.value = client_award.value


class ProgramAwardDelete(BasePydantic):
    ok: bool
    Deleted: SegmentAwardModelDB
