from tests.testutil import new_client_award, update_client_award, new_award


def test_integration_get_client_awards(test_app, client_award):
	response = test_app.get(f"/v1/clients/{client_award['client_uuid']}/awards")
	assert response.status_code == 200
	response = response.json()["items"][0]
	assert len(response["client_award_9char"]) == 9
	assert response["description"] == client_award["description"]
	assert response["name"] == client_award["name"]
	assert client_award["award_uuid"] == new_award["uuid"]


def test_integration_get_client_award(test_app, client_award):
	response = test_app.get(f"/v1/clients/{client_award['client_uuid']}/awards/{client_award['client_award_9char']}")
	assert response.status_code == 200
	response = response.json()
	assert response["client_award_9char"] == client_award["client_award_9char"]
	assert response["description"] == client_award["description"]
	assert response["name"] == client_award["name"]
	assert client_award["award_uuid"] == new_award["uuid"]


def test_integration_create_client_award(client_award):
	assert len(client_award["client_award_9char"]) == 9
	assert client_award["award_uuid"] == new_award["uuid"]
	assert client_award["uuid"] == client_award['client_uuid'] + client_award['client_award_9char']


def test_integration_update_client_award(test_app, client_award):
	response = test_app.put(f"/v1/clients/{client_award['client_uuid']}/awards/{client_award['client_award_9char']}", json=update_client_award)
	assert response.status_code == 200
	response = response.json()
	assert response["client_award_9char"] == client_award["client_award_9char"]
	assert response["name"] == update_client_award["name"]
	assert response["description"] == update_client_award["description"]
	


def test_integration_delete_client_award(test_app, client_award):
	response = test_app.delete(f"/v1/clients/{client_award['client_uuid']}/awards/{client_award['client_award_9char']}")
	assert response.status_code == 200
	response = response.json()
	assert response["ok"] == True
	assert response["Deleted"]["client_award_9char"] == client_award["client_award_9char"]
	assert response["Deleted"]["client_uuid"] == client_award["client_uuid"]
