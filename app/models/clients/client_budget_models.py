from typing import Optional
from pydantic import validator
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.enums import BudgetType
from app.models.base_class import Base, BasePydantic
from app.models.clients.clients_models import ClientModel
from sqlalchemy.dialects import mysql
Integer = mysql.INTEGER


class ClientBudgetModelDB(Base):
    __tablename__ = "client_budget"

    uuid: Mapped[str] = mapped_column(String(65), default=None, primary_key=True, index=True)
    client_uuid: Mapped[str] = mapped_column(String(56), default=None, index=True, nullable=True)
    budget_9char: Mapped[str] = mapped_column(String(9), default=None, index=True, nullable=True)
    parent_9char: Mapped[str] = mapped_column(String(9), default=None, index=True, nullable=True)
    name: Mapped[str] = mapped_column(String(255), default=None, nullable=True)
    value: Mapped[int] = mapped_column(Integer(11), default=0, nullable=True)
    time_created: Mapped[int] = mapped_column(Integer(11), default=None, nullable=True)
    time_updated: Mapped[int] = mapped_column(Integer(11), default=None, nullable=True)
    active: Mapped[bool] = mapped_column(default=True, nullable=True)
    budget_type: Mapped[int] = mapped_column(Integer(11), default=0, nullable=True)


class ClientBudgetModel(BasePydantic):
    uuid: Optional[str]
    client_uuid: Optional[str]
    budget_9char: Optional[str]
    parent_9char: Optional[str]
    name: Optional[str]
    value: Optional[int]
    time_created: Optional[int]
    time_updated: Optional[int]
    active: Optional[bool]
    budget_type: Optional[BudgetType]


class ClientBudgetCreate(BasePydantic):
    budget_9char: Optional[str]
    parent_9char: Optional[str]
    name: Optional[str]
    value: int
    active: Optional[bool] = True
    budget_type: Optional[BudgetType]

    @validator('budget_type', pre=False)
    def validate_award_type(cls, v, field):
        return field.type_[v].value


class ClientBudgetUpdate(BasePydantic):
    name: Optional[str]
    value: Optional[int] = 0
    parent_9char: Optional[str]
    time_updated: Optional[int] = 0
    active: Optional[bool]
    budget_type: Optional[BudgetType]

    @validator('budget_type', pre=False)
    def validate_award_type(cls, v, field):
        return field.type_[v].value


class ClientBudgetExpanded(ClientBudgetModel):
    client: Optional[ClientModel]
    subbudgets_expanded: Optional[list[ClientBudgetModel]]

class ClientBudgetShortExpand(ClientBudgetModel):
    client: Optional[ClientModel]
    subbudgets: Optional[ClientBudgetModel]


class BudgetResponse(ClientBudgetModel):
    pass


class BudgetDelete(BasePydantic):
    ok: bool = True
    Deleted: ClientBudgetModel


class DeleteResponse(BasePydantic):
    ok: bool = True
    Deleted: ClientBudgetModel
    Parent: Optional[ClientBudgetModel]

    @classmethod
    def format_data(cls, values):
        if isinstance(values, list):
            temp_dict = values[0]
            temp_dict['Parent'] = values[1]
            return temp_dict
        elif isinstance(values, ClientBudgetModelDB):
            values = {'Deleted': values}
        return values
