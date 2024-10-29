from typing import Optional
from pydantic import validator
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.enums import Status
from app.models.base_class import Base, BasePydantic
from sqlalchemy.dialects import mysql
Integer = mysql.INTEGER


class SegmentModelDB(Base):
    __tablename__ = "program_segment"

    uuid: Mapped[str] = mapped_column(String(72), default=None, primary_key=True, index=True)
    client_uuid: Mapped[str] = mapped_column(String(56), default=None, index=True, nullable=True)
    program_9char: Mapped[str] = mapped_column(String(9), default=None, index=True, nullable=True)
    segment_9char: Mapped[str] = mapped_column(String(9), default=None, index=True, nullable=True)
    budget_9char: Mapped[str] = mapped_column(String(9), default=None, index=True, nullable=True)
    name: Mapped[str] = mapped_column(String(255), default=None, nullable=True)
    description: Mapped[str] = mapped_column(Text, default=None, nullable=True)
    status: Mapped[int] = mapped_column(Integer(4), default=None, index=True, nullable=True)
    time_created: Mapped[int] = mapped_column(Integer(11), default=None, nullable=True)
    time_updated: Mapped[int] = mapped_column(Integer(11), default=None, nullable=True)


class SegmentModel(BasePydantic):
    uuid: str
    client_uuid: str
    program_9char: str
    segment_9char: str
    budget_9char: Optional[str]
    name: Optional[str]
    description: Optional[str]
    status: Optional[Status]
    time_created: Optional[int]
    time_updated: Optional[int]


class SegmentResponse(SegmentModel):
    pass


class SegmentUpdate(BasePydantic):
    name: Optional[str]
    description: Optional[str]
    budget_9char: Optional[str]
    status: Optional[Status]

    @validator('status', pre=False)
    def validate_award_type(cls, v, field):
        return field.type_[v].value


class SegmentCreate(BasePydantic):
    budget_9char: Optional[str]
    name: Optional[str]
    description: Optional[str]
    status: Optional[Status]

    @validator('status', pre=False)
    def validate_award_type(cls, v, field):
        return field.type_[v].value


class SegmentDelete(BasePydantic):
    ok: bool
    Deleted: SegmentModel
