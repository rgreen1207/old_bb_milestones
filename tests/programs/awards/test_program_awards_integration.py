from tests.testutil import new_program_award, new_client_award, update_program_award


def test_integration_get_program_awards(test_app, program_award):
	response = test_app.get(f"/v1/clients/{program_award['client_uuid']}/programs/{program_award['program_9char']}/awards")
	assert response.status_code == 200
	response = response.json()["items"][0]
	assert len(response["program_award_9char"]) == 9
	assert response["description"] == program_award["description"]
	assert response["client_award_description"] == new_client_award["description"]


def test_integration_get_program_award(test_app, program_award):
	response = test_app.get(f"/v1/clients/{program_award['client_uuid']}/programs/{program_award['program_9char']}/awards/{program_award['program_award_9char']}")
	assert response.status_code == 200
	response = response.json()
	assert response["program_award_9char"] == program_award["program_award_9char"]
	assert response["description"] == program_award["description"]
	assert response["client_award_description"] == new_client_award["description"]


def test_integration_create_program_award(program_award, client_award):
	assert len(program_award["program_award_9char"]) == 9
	assert program_award["client_award_9char"] == client_award["client_award_9char"]
	assert program_award["uuid"] == program_award['client_uuid'] + program_award['program_9char'] + program_award['client_award_9char']


def test_integration_update_program_award(test_app, program_award):
	response = test_app.put(f"/v1/clients/{program_award['client_uuid']}/programs/{program_award['program_9char']}/awards/{program_award['program_award_9char']}", json=update_program_award)
	assert response.status_code == 200
	response = response.json()
	assert response["program_award_9char"] == program_award["program_award_9char"]
	assert response["client_award_description"] == new_client_award["description"]
	assert response["name"] == update_program_award["name"]
	assert response["description"] == update_program_award["description"]
	


def test_integration_delete_program_award(test_app, program_award):
	response = test_app.delete(f"/v1/clients/{program_award['client_uuid']}/programs/{program_award['program_9char']}/awards/{program_award['program_award_9char']}")
	assert response.status_code == 200
	response = response.json()
	assert response["ok"] == True
	assert response["Deleted"]["program_award_9char"] == program_award["program_award_9char"]
	assert response["Deleted"]["client_uuid"] == program_award["client_uuid"]
