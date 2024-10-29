from enum import IntEnum, Enum
from typing import Optional
from pydantic import Field
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base_class import Base, BasePydantic
from sqlalchemy.dialects import mysql
Integer = mysql.INTEGER


# TODO: finalize what permissions are needed/wanted
class AdminPermissions(IntEnum):
    none = 0
    supervisor = 1
    manager = 2

class ProgramAdminStatus(Enum):
    exists = "existing admin"
    created = "admin created"


class AdminModelDB(Base):
    __tablename__ = "program_admin"

    uuid: Mapped[str] = mapped_column(String(56), default=None, primary_key=True, index=True)
    program_uuid: Mapped[Optional[str]] = mapped_column(String(65), default=None, index=True, nullable=True)
    client_uuid: Mapped[Optional[str]] = mapped_column(String(56), default=None, index=True, nullable=True)
    program_9char: Mapped[Optional[str]] = mapped_column(String(9), default=None, index=True, nullable=True)
    user_uuid: Mapped[Optional[str]] = mapped_column(String(56), default=None, index=True, nullable=True)
    permissions: Mapped[Optional[int]] = mapped_column(Integer(11), default=0, index=True, nullable=True)
    time_created: Mapped[Optional[int]] = mapped_column(Integer(11), default=None, nullable=True)
    time_updated: Mapped[Optional[int]] = mapped_column(Integer(11), default=None, nullable=True)

class AdminModel(BasePydantic):
    uuid: Optional[str]
    program_uuid: Optional[str]
    client_uuid: Optional[str]
    program_9char: Optional[str]
    user_uuid: Optional[str]
    permissions: Optional[int]
    time_created: Optional[int]
    time_updated: Optional[int]

class AdminCreate(BasePydantic):
    program_uuid: Optional[str]
    user_uuid: str
    permissions: Optional[int]

class AdminStatus(AdminModel):
    status: Optional[ProgramAdminStatus] = Field(description="This mapped_column can have the values 'exists' or 'admin created'.")

class AdminUpdate(BasePydantic):
    permissions: Optional[int]


class AdminDelete(BasePydantic):
    ok: bool
    Deleted: AdminModel
