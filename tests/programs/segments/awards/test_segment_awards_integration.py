from tests.testutil import new_segment_award, update_segment_award


def test_integration_get_segment_awards(test_app, segment_award):
	response = test_app.get(f"/v1/clients/{segment_award['client_uuid']}/programs/{segment_award['program_9char']}/segments/{segment_award['segment_9char']}/awards")
	assert response.status_code == 200
	response = response.json()["items"][0]
	assert len(response["segment_award_9char"]) == 9
	assert response["program_award_9char"] == segment_award["program_award_9char"]
	assert response["client_award_9char"] == segment_award["client_award_9char"]
	assert response["name"] == segment_award["name"]
	assert response["description"] == segment_award["description"]


def test_integration_get_segment_award(test_app, segment_award):
	response = test_app.get(f"/v1/clients/{segment_award['client_uuid']}/programs/{segment_award['program_9char']}/segments/{segment_award['segment_9char']}/awards/{segment_award['segment_award_9char']}")
	assert response.status_code == 200
	response = response.json()
	assert response["program_award_9char"] == segment_award["program_award_9char"]
	assert response["description"] == segment_award["description"]
	assert response["name"] == segment_award["name"]
	assert response["program_award_9char"] == segment_award["program_award_9char"]
	assert response["client_award_9char"] == segment_award["client_award_9char"]


def test_integration_create_segment_award(program_award, segment_award):
	assert len(segment_award["segment_award_9char"]) == 9
	assert segment_award["client_award_9char"] == program_award["client_award_9char"]
	assert segment_award["program_award_9char"] == program_award["program_award_9char"]
	assert segment_award["uuid"] == segment_award['client_uuid'] + segment_award['program_9char'] + segment_award["segment_9char"] + segment_award['client_award_9char']


def test_integration_update_segment_award(test_app, segment_award):
	response = test_app.put(f"/v1/clients/{segment_award['client_uuid']}/programs/{segment_award['program_9char']}/segments/{segment_award['segment_9char']}/awards/{segment_award['segment_award_9char']}", json=update_segment_award)
	assert response.status_code == 200
	response = response.json()
	assert response["program_award_9char"] == segment_award["program_award_9char"]
	assert response["client_award_9char"] == segment_award["client_award_9char"]
	assert response["name"] == update_segment_award["name"]
	assert response["description"] == update_segment_award["description"]
	
def test_integration_delete_segment_award(test_app, segment_award):
	response = test_app.delete(f"/v1/clients/{segment_award['client_uuid']}/programs/{segment_award['program_9char']}/segments/{segment_award['segment_9char']}/awards/{segment_award['segment_award_9char']}")
	assert response.status_code == 200
	response = response.json()
	assert response["ok"] == True
	assert response["Deleted"]["program_award_9char"] == segment_award["program_award_9char"]
	assert response["Deleted"]["client_uuid"] == segment_award["client_uuid"]
	assert response["Deleted"]["program_9char"] == segment_award["program_9char"]
	assert response["Deleted"]["segment_9char"] == segment_award["segment_9char"]