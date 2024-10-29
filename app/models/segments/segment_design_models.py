from typing import Optional
from pydantic import validator
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.enums import ChannelType, Status
from app.models.base_class import Base, BasePydantic
from sqlalchemy.dialects import mysql
Integer = mysql.INTEGER


class SegmentDesignModelDB(Base):
    __tablename__ = "program_segment_design"

    uuid: Mapped[str] = mapped_column(String(81), default=None, primary_key=True, index=True)
    program_uuid: Mapped[str] = mapped_column(String(65), default=None, index=True, nullable=True)
    client_uuid: Mapped[str] = mapped_column(String(56), default=None, index=True, nullable=True)
    program_9char: Mapped[str] = mapped_column(String(9), default=None, index=True, nullable=True)
    segment_9char: Mapped[str] = mapped_column(String(9), default=None, index=True, nullable=True)
    design_9char: Mapped[str] = mapped_column(String(9), default=None, index=True, nullable=True)
    message_uuid: Mapped[str] = mapped_column(String(56), default=None, index=True, nullable=True)
    channel: Mapped[int] = mapped_column(Integer(11), default=None, index=True, nullable=True)
    status: Mapped[int] = mapped_column(Integer(11), default=None, index=True, nullable=True)
    time_created: Mapped[int] = mapped_column(Integer(11), default=None, nullable=True)
    time_updated: Mapped[int] = mapped_column(Integer(11), default=None, nullable=True)


class SegmentDesignModel(BasePydantic):
    uuid: str
    client_uuid: str
    program_9char: str
    segment_9char: str
    design_9char: str
    program_uuid: Optional[str]
    message_uuid: Optional[str]
    channel: Optional[ChannelType]
    status: Optional[Status]
    time_created: Optional[int]
    time_updated: Optional[int]


class SegmentDesignResponse(SegmentDesignModel):
    pass


class SegmentDesignCreate(BasePydantic):
    message_uuid: Optional[str]
    channel: Optional[ChannelType]
    status: Optional[Status]

    @validator("status", pre=False)
    def validate_award_type(cls, v, field):
        return field.type_[v].value


class SegmentDesignUpdate(BasePydantic):
    channel: Optional[ChannelType]
    status: Optional[Status]

    @validator("status", pre=False)
    def validate_award_type(cls, v, field):
        return field.type_[v].value


class SegmentDesignDelete(BasePydantic):
    ok: bool
    Deleted: SegmentDesignModel
