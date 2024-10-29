from tests.testutil import new_program_admin, update_program_admin

def test_integration_create_program_admin(program_admin):
	assert new_program_admin["program_uuid"] == program_admin["program_uuid"]
	assert "uuid" in program_admin
	assert program_admin["permissions"] == new_program_admin["permissions"]
	assert program_admin["status"] == "admin created"


def test_integration_get_program_admins(test_app, program_admin):
	response = test_app.get(f"/v1/clients/{program_admin['client_uuid']}/programs/{program_admin['program_9char']}/admins")
	assert response.status_code == 200
	response = response.json()["items"][0]
	assert program_admin["client_uuid"] == response["client_uuid"]
	assert program_admin["program_9char"] == response["program_9char"]
	assert program_admin["program_uuid"] == response["program_uuid"]
	

def test_integration_get_program_admin(test_app, program_admin):
	response = test_app.get(f"/v1/clients/{program_admin['client_uuid']}/programs/{program_admin['program_9char']}/admins/{program_admin['user_uuid']}")
	assert response.status_code == 200
	response = response.json()
	assert program_admin["uuid"] == response["uuid"]
	assert program_admin["user_uuid"] == response["user_uuid"]


def test_integration_update_program_admin(test_app, program_admin):
	response = test_app.put(f"/v1/clients/{program_admin['client_uuid']}/programs/{program_admin['program_9char']}/admins/{program_admin['user_uuid']}", json=update_program_admin)
	assert response.status_code == 200
	response = response.json()
	assert program_admin["client_uuid"] == response["client_uuid"]
	assert program_admin["program_9char"] == response["program_9char"]
	assert program_admin["program_uuid"] == response["program_uuid"]
	assert response["permissions"] == update_program_admin["permissions"]


def test_integration_delete_program_admin(test_app, program_admin):
	response = test_app.delete(f"/v1/clients/{program_admin['client_uuid']}/programs/{program_admin['program_9char']}/admins/{program_admin['user_uuid']}")
	assert response.status_code == 200
	response = response.json()
	assert response["ok"] == True
	assert response["Deleted"]["user_uuid"] == program_admin["user_uuid"]
