from tests.testutil import new_client_user, update_client_user


def test_integration_create_client_user(client_user):
	assert "uuid" in client_user
	assert "client_uuid" in client_user

def test_integration_get_client_users(test_app, client_user):
	response = test_app.get(f"/v1/clients/{client_user['client_uuid']}/users")
	assert response.status_code == 200
	response = response.json()["items"][0]
	assert response['client_uuid'] == client_user['client_uuid']
	assert response['uuid'] == client_user['uuid']

def test_integration_get_client_user(test_app, client_user):
	response = test_app.get(f"/v1/clients/{client_user['client_uuid']}/users/{client_user['user_uuid']}")
	assert response.status_code == 200
	response = response.json()
	assert "uuid" in response
	assert response["client_uuid"] == client_user["client_uuid"]
	assert response["user_uuid"] == client_user["user_uuid"]

def test_integration_update_client_user(test_app, client_user):
	response = test_app.put(f"/v1/clients/{client_user['client_uuid']}/users/{client_user['uuid']}", json=update_client_user)
	assert response.status_code == 200
	response = response.json()
	assert response["client_uuid"] == client_user["client_uuid"]
	assert response["uuid"] == client_user["uuid"]
	assert response["title"] == update_client_user["title"]
	assert response["department"] == update_client_user["department"]


def test_integration_delete_client_user(test_app, client):
	client_user = test_app.post(f"/v1/clients/{client['uuid']}/users", json=new_client_user)
	client_user = client_user.json()
	user = test_app.get(f"/v1/users/{client_user['user_uuid']}?expand_services=true")
	user = user.json()
	service_uuid = user["services"]["email"][0]["uuid"]
	try:
		assert client_user["client_uuid"] == client["uuid"]
		response = test_app.delete(f"/v1/clients/{client['uuid']}/users/{client_user['uuid']}")
		assert response.status_code == 200
		response = response.json()
		assert response["ok"] == True
		assert response["Deleted"]["uuid"] == client_user["uuid"]
	finally:
		test_app.delete(f"/v1/clients/{client['uuid']}/users/{client_user['uuid']}")
		test_app.delete(f"/v1/users/{user['uuid']}/services/{service_uuid}")
		test_app.delete(f"/v1/users/{user['uuid']}")
