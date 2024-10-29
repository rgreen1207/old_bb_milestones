from typing import Optional
from pydantic import validator
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.enums import ChannelType, MessageType, Status
from app.models.base_class import Base, BasePydantic
from sqlalchemy.dialects import mysql
Integer = mysql.INTEGER

# see enums.py for message_types enum class
message_types = {
    1: "welcome",
    2: "auth",
    3: "award",
    4: "anniversary",
    5: "birthday",
    6: "redeem",
    7: "message",
    8: "reminder",
    9: "survey"
}

class MessageModelDB(Base):
    __tablename__ = "message"

    uuid: Mapped[str] = mapped_column(String(83), default=None, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), default=None)
    message_uuid: Mapped[str] = mapped_column(String(74), default=None, index=True, nullable=True)
    client_uuid: Mapped[str] = mapped_column(String(56), default=None, index=True, nullable=True)
    message_9char: Mapped[str] = mapped_column(String(9), default=None, index=True, nullable=True)
    program_9char: Mapped[str] = mapped_column(String(9), default=None, index=True, nullable=True)
    segment_9char: Mapped[str] = mapped_column(String(9), default=None, index=True, nullable=True)
    message_type: Mapped[int] = mapped_column(Integer(11), default=1, nullable=True)
    # Options: 1 = email, 2 = text, 4 = slack, 8 = ms teams, 16 = web
    channel: Mapped[int] = mapped_column(Integer(11), default=None, nullable=True)
    status: Mapped[int] = mapped_column(Integer(11), default=1, nullable=True)
    body: Mapped[str] = mapped_column(Text, default=None, nullable=True)
    time_created: Mapped[int] = mapped_column(Integer(11), default=None, nullable=True)
    time_updated: Mapped[int] = mapped_column(Integer(11), default=None, nullable=True)


class MessageModel(BasePydantic):
    uuid: Optional[str]
    name: Optional[str]
    message_9char: Optional[str]
    body: Optional[str]
    channel: Optional[ChannelType]
    message_uuid: Optional[str]
    client_uuid: Optional[str]
    program_9char: Optional[str]
    segment_9char: Optional[str]
    message_type: Optional[MessageType]
    status: Optional[Status]
    time_created: Optional[int]
    time_updated: Optional[int]


class MessageResponse(MessageModel):
    pass


class MessageCreate(BasePydantic):
    name: str
    body: Optional[str]
    channel: ChannelType
    message_uuid: Optional[str]
    client_uuid: Optional[str]
    program_9char: Optional[str]
    segment_9char: Optional[str]
    message_type: MessageType
    status: Optional[Status]

    @validator("message_type", "status", pre=False)
    def validate_award_type(cls, v, field):
        return field.type_[v].value


class MessageUpdate(BasePydantic):
    name: Optional[str]
    message_type: Optional[MessageType]
    channel: Optional[ChannelType]
    status: Optional[Status]
    body: Optional[str]

    @validator("message_type", "status", pre=False)
    def validate_award_type(cls, v, field):
        return field.type_[v].value


class MessageRecipient(BasePydantic):
    client_user_uuid: str
    anniversary: Optional[int]
    award_uuid: str


class MessageSend(BasePydantic):
    client_uuid: str
    recipients: list[MessageRecipient]


class MessageDelete(BasePydantic):
    ok: bool
    Deleted: MessageModel
