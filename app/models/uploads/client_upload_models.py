from enum import Enum
from app.models.base_class import BasePydantic


class UploadType(Enum):
    IMAGE = "image"
    ROSTER = "roster"

    def __repr__(self):
        return self.value

    def __eq__(self, other):
        return self.value == other

    def __hash__(self):
        return hash(self.value)



class UploadFile(BasePydantic):
    file_name: str


class Uploadread(BasePydantic):
    first_name: str
    last_name: str
    work_email: str
    personal_email: str
    cell_phone: str
    time_hire: str
    time_start: str
    time_birthday: str
    employee_id: str
    manager_id: str
    cost_center_id: str
    worker_type: str
    department: str
    manager_name: str
    location: str
    title: str
    department_lead_id: str
