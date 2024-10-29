import pytest

from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from app.models.clients.clients_models import ClientModelDB
from app.routers.v1.clients.client_router import router as clients_router
from app.routers.v1.v1CommonRouting import CommonRoutes

@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(clients_router)
    return TestClient(app)

def test_get_clients(monkeypatch, client):
    async def mock_get_all(model):
        return [
            ClientModelDB(
                uuid="1234-5678-9012",
                name="Client A",
                description="Sample Client A",
                time_created=0,
                time_updated=0,
                time_ping=0,
            ),
            ClientModelDB(
                uuid="5678-9012-3456",
                name="Client B",
                description="Sample Client B",
                time_created=0,
                time_updated=0,
                time_ping=0,
            ),
        ]
    # monkeypatch to replace the get_all method from CommonRoutes with the mocked out version
    monkeypatch.setattr(CommonRoutes, "get_all", mock_get_all)
    response = client.get("/clients")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "uuid": "1234-5678-9012",
            "name": "Client A",
            "description": "Sample Client A",
            "time_created": 0,
            "time_updated": 0,
            "time_ping": 0,
        },
        {
            "uuid": "5678-9012-3456",
            "name": "Client B",
            "description": "Sample Client B",
            "time_created": 0,
            "time_updated": 0,
            "time_ping": 0,
        },
    ]

def test_get_client(monkeypatch, client):
    async def mock_get_one(model, search_by):
        return ClientModelDB(
            uuid="1234-5678-9012",
            name="Client A",
            description="Sample Client A",
            time_created=0,
            time_updated=0,
            time_ping=0,
        )
    monkeypatch.setattr(CommonRoutes, "get_one", mock_get_one)
    client_uuid = "1234-5678-9012"
    # makes a get request to the specific url, whichever function is attacthed to that route will then run.
    response = client.get(f"/clients/{client_uuid}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "uuid": "1234-5678-9012",
        "name": "Client A",
        "description": "Sample Client A",
        "time_created": 0,
        "time_updated": 0,
        "time_ping": 0,
    }

def test_create_client(monkeypatch, client):
    request_data1 = {
        "uuid": "5678-9012-3456",
        "name": "Client B",
        "description": "Sample Client B",
        "time_created": 1,
        "time_updated": 1,
        "time_ping": 1,
    }
    response_data1 = request_data1
    async def mock_create_one_or_many(items: (list[ClientModelDB] | ClientModelDB)):
        if isinstance(items, list):
            return items
        else:
            return response_data1
    monkeypatch.setattr(CommonRoutes, "create_one_or_many", mock_create_one_or_many)
    # tests for a single client
    response = client.post("/clients", json=request_data1)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == response_data1

def test_create_clients(monkeypatch, client):
    request_data1 = {
        "uuid": "5678-9012-3456",
        "name": "Client B",
        "description": "Sample Client B",
        "time_created": 1,
        "time_updated": 1,
        "time_ping": 1,
    }
    request_data2 = {
        "uuid": "1234-5678-9012",
        "name": "Client A",
        "description": "Sample Client A",
        "time_created": 1,
        "time_updated": 1,
        "time_ping": 1,
    }
    response_data1 = request_data1
    response_data2 = request_data2
    async def mock_create_one_or_many(items: (list[ClientModelDB] | ClientModelDB)):
        if isinstance(items, list):
            return items
        else:
            return response_data1
    monkeypatch.setattr(CommonRoutes, "create_one_or_many", mock_create_one_or_many)
    # tests for a list of clients
    response = client.post("/clients", json=[request_data1, request_data2])
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [response_data1, response_data2]

def test_update_client_by_uuid(monkeypatch, client):
    # Test data
    client_uuid = "5678-9012-3456"
    request_data = {
        "uuid": client_uuid,
        "name": "Client B",
        "description": "Sample Client B",
        "time_created": 1,
        "time_updated": 1,
        "time_ping": 1,
    }
    update_data = {
        "name": "Updated Client B",
        "description": "Updated Sample Client B",
        "time_updated": 2,
    }
    response_data = {
        **request_data,
        **update_data,
    }
    # Mock function
    async def mock_update_one(search_by, original_model, update_model):
        if search_by == client_uuid:
            updated_fields = update_model.dict(exclude_unset=True)
            return {**request_data, **updated_fields}
        else:
            return None
    # Patch the update_one function
    monkeypatch.setattr(CommonRoutes, "update_one", mock_update_one)
    # Test the route
    response = client.put(f"/clients/{client_uuid}", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == response_data

def test_delete_client_by_uuid(monkeypatch, client):
    # Test data
    request_client_uuid = "5678-9012-3456"
    request_data = {
        "uuid": request_client_uuid,
        "name": "Client B",
        "description": "Sample Client B",
        "time_created": 1,
        "time_updated": 1,
        "time_ping": 1,
    }
    async def mock_delete_one(client_uuid, model):
        if client_uuid == request_client_uuid:
            return {"ok": True, "Deleted": request_data}
        else:
            return {"status":"404", "Description":"Not found"}
    monkeypatch.setattr(CommonRoutes, "delete_one", mock_delete_one)

    response = client.delete(f"/clients/{request_client_uuid}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"ok": True, "Deleted": request_data}
