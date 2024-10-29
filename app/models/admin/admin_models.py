from app.models.base_class import BasePydantic

class AdminCreate(BasePydantic):
    first_name: str
    last_name: str
    email_address: str
    # client_uuid_list: list[str]
    # service_uuid: str # "email" or "cell"
    # service_user_id: str # email address or cell phone number
    # admin: int


class AdminClientSwap(BasePydantic):
    client_uuid: str
