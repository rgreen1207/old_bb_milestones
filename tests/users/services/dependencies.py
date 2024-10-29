import pytest
from typing import Union
from fastapi import Depends, HTTPException
from fastapi.testclient import TestClient
from app.actions.users.services import UserServiceActions
#from app.models.users import UserService, UserServiceCreate, ServiceStatus
from app.main import app

client = TestClient(app)

# Sample data
user_uuid = "12345"
service_uuid = "email"
service_user_id = "test@example.com"

# Helper function to simulate check_existing function
async def mock_check_existing(user_service: UserServiceCreate) -> Union[UserService, UserServiceCreate]:
    if user_service.service_user_id == service_user_id:
        return UserService(
            user_uuid=user_uuid,
            service_uuid=service_uuid,
            service_user_id=service_user_id,
            service_user_screenname="Test User",
            service_user_name="Test User",
            service_access_token="test_access_token",
            service_access_secret="test_access_secret",
            service_refresh_token="test_refresh_token",
            time_created=0,
            time_updated=0,
            uuid="test_uuid",
        )
    else:
        return user_service

# Test fixture to override the original check_existing dependency
@pytest.fixture
def override_check_existing():
    app.dependency_overrides[UserServiceActions.check_existing] = mock_check_existing
