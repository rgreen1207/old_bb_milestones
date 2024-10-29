from fastapi.testclient import TestClient
import tests.testutil as utils


def test_get_awards(test_app: TestClient, award: dict):
	response = test_app.get(f"/v1/awards")
	assert response.status_code == 200
	all_awards = response.json()["items"]
	for award_to_check in all_awards:
		test_award = award_to_check if award_to_check["uuid"] == award["uuid"] else None
		if test_award:
			break
	assert test_award["uuid"] == award["uuid"]
	assert test_award["description"] == award["description"]
	assert test_award["name"] == award["name"]


def test_get_award(test_app, award):
	response = test_app.get(f"/v1/awards/{award['uuid']}")
	assert response.status_code == 200
	response = response.json()
	assert response["description"] == award["description"]
	assert response["name"] == award["name"]
	assert response["uuid"] == award["uuid"]


def test_create_award(award):
	assert "uuid" in award
	assert award["name"] == utils.new_award['name']
	assert award["description"] == utils.new_award["description"]
	assert award["channel"] == utils.new_award['channel']
	assert award["award_type"] == "recognition"
	assert award["value"] == utils.new_award['value']


def test_update_award(test_app, award):
	response = test_app.put(f"/v1/awards/{award['uuid']}", json=utils.update_award)
	assert response.status_code == 200
	response = response.json()
	assert response["name"] == utils.update_award["name"]
	assert response["description"] == utils.update_award["description"]
	assert response["hero_image"] == "jpeg"
	assert response["channel"] == utils.update_award["channel"]
	assert response["award_type"] == "reward"
	assert response["value"] == utils.update_award["value"]


def test_delete_award(test_app, award):
	response = test_app.delete(f"/v1/awards/{award['uuid']}")
	assert response.status_code == 200
	response = response.json()
	assert response["ok"] == True
	assert response["Deleted"]["uuid"] == award["uuid"]
