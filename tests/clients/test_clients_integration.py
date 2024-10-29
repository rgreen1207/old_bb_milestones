from tests.testutil import single_client, list_of_clients


def test_integration_get_client(test_app, client):
	response = test_app.get(f"/v1/clients/{client['uuid']}")
	assert response.status_code == 200
	assert response.json()['uuid'] == client['uuid']


def test_integration_get_clients(test_app, clients):
	response = test_app.get(f"/v1/clients")
	clients_from_get = response.json()["items"]
	assert response.status_code == 200
	for client in clients_from_get:
		assert client["uuid"] == clients[0]["uuid"] or clients[1]["uuid"]


def test_integration_create_client(client):
	assert "uuid" in client
	assert client['name'] == single_client['name']
	assert client['description'] == single_client['description']
	assert "time_created" in client
	assert "time_updated" in client
	assert "time_ping" in client


def test_integration_create_clients(clients):
	assert clients[0]["uuid"] != clients[1]["uuid"]
	for i,client in enumerate(clients):
		assert client['name'] == list_of_clients[i]['name']
		assert client['description'] == list_of_clients[i]['description']
		assert "time_created" in client
		assert "time_updated" in client
		assert "time_ping" in client


def test_integration_update_client_by_uuid(test_app, client):
	info_to_update = {
		"name": "updated",
		"description": "updated",
	}
	response = test_app.put(f"/v1/clients/{client['uuid']}", json=info_to_update)
	updated_client = response.json()
	assert response.status_code == 200
	assert updated_client['uuid'] == client['uuid']
	assert updated_client['name'] == "updated"
	assert updated_client['description'] == "updated"


def test_integration_delete_client_by_uuid(test_app, client):
	response = test_app.delete(f"/v1/clients/{client['uuid']}")
	assert response.status_code == 200
	assert response.json()["ok"] == True
	assert response.json()['Deleted']['uuid'] == client['uuid']
