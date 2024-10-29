from typing import Optional
from pydantic import validator
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.enums import Cadence, CadenceValue, Status, ProgramType
from app.models.base_class import Base, BasePydantic
from sqlalchemy.dialects import mysql
Integer = mysql.INTEGER


class ProgramModelDB(Base):
    __tablename__ = "program"

    uuid: Mapped[str] = mapped_column(String(65), default=None, primary_key=True, index=True)
    user_uuid: Mapped[str] = mapped_column(String(56), default=None, index=True, nullable=True)
    program_9char: Mapped[str] = mapped_column(String(9), default=None, index=True, nullable=True)
    name: Mapped[str] = mapped_column(String(255), default=None, index=True, nullable=True)
    description: Mapped[str] = mapped_column(Text, default=None, index=True, nullable=True)
    client_uuid: Mapped[str] = mapped_column(String(56), default=None, index=True, nullable=True)
    budget_9char: Mapped[str] = mapped_column(String(56), default=None, index=True, nullable=True)
    status: Mapped[int] = mapped_column(Integer(11), default=None, index=True, nullable=True)
    program_type: Mapped[int] = mapped_column(Integer(11), default=None, index=True, nullable=True)
    cadence: Mapped[int] = mapped_column(Integer(11), default=None, index=True, nullable=True)
    cadence_value: Mapped[int] = mapped_column(Integer(11), default=None, index=True, nullable=True)
    time_created: Mapped[int] = mapped_column(Integer(11), default=None, nullable=True)
    time_updated: Mapped[int] = mapped_column(Integer(11), default=None, nullable=True)


class ProgramModel(BasePydantic):
    uuid: Optional[str]
    user_uuid: Optional[str]
    program_9char: Optional[str]
    name: Optional[str]
    description: Optional[str]
    client_uuid: Optional[str]
    budget_9char: Optional[str]
    status: Optional[Status]
    program_type: Optional[ProgramType]
    cadence: Optional[Cadence]
    cadence_value: Optional[CadenceValue]
    time_created: Optional[int]
    time_updated: Optional[int]


class ProgramResponse(ProgramModel):
    pass


class ProgramCreate(BasePydantic):
    user_uuid: str
    name: str
    description: Optional[str]
    budget_9char: Optional[str]
    status: Optional[Status]
    program_type: Optional[ProgramType]
    cadence: Cadence
    cadence_value: Optional[CadenceValue]

    @validator(
            "status",
            "program_type",
            "cadence",
            "cadence_value",
            pre=False
        )
    def validate_award_type(cls, v, field):
        return field.type_[v].value


class ProgramUpdate(BasePydantic):
    name: Optional[str]
    description: Optional[str]
    budget_9char: Optional[str]
    status: Optional[Status]
    program_type: Optional[ProgramType]
    cadence: Optional[Cadence]
    cadence_value: Optional[CadenceValue]

    @validator(
            "status",
            "program_type",
            "cadence",
            "cadence_value",
            pre=False
        )
    def validate_award_type(cls, v, field):
        return field.type_[v].value


class ProgramDelete(BasePydantic):
    ok: bool
    Deleted: ProgramModel
