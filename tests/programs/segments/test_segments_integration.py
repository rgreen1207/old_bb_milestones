from fastapi.testclient import TestClient
import tests.testutil as utils


def test_get_all_segments(test_app: TestClient, segment: dict):
	response = test_app.get(f"/v1/clients/{segment['client_uuid']}/programs/{segment['program_9char']}/segments")
	assert response.status_code == 200
	assert response.json()["items"][0]["name"] == segment["name"]


def test_get_segment(test_app: TestClient, segment: dict):
	response = test_app.get(
		f"/v1/clients/{segment['client_uuid']}/programs/{segment['program_9char']}/segments/{segment['segment_9char']}"
	)
	assert response.status_code == 200
	assert response.json()["name"] == segment["name"]


def test_create_segment(segment: dict):
	assert "uuid" in segment
	assert segment["name"] == utils.new_program_segment["name"]


def test_update_segment(test_app: TestClient, segment: dict):
	response = test_app.put(
		f"/v1/clients/{segment['client_uuid']}/programs/{segment['program_9char']}/segments/{segment['segment_9char']}",
		json = utils.update_program_segment
	)
	assert response.status_code == 200
	assert response.json()["name"] == utils.update_program_segment["name"]


def test_delete_segment(test_app: TestClient, segment: dict):
	response = test_app.delete(
		f"/v1/clients/{segment['client_uuid']}/programs/{segment['program_9char']}/segments/{segment['segment_9char']}"
	)
	assert response.status_code == 200
	assert response.json()["ok"] == True
