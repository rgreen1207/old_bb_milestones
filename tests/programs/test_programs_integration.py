
def test_integration_create_program(program):
    assert "client_uuid" in program
    assert "uuid" in program
    assert "user_uuid" in program
    assert program['name'] == "Pytest Blueboard 2023 Anniversary Program"


def test_integration_get_programs(test_app, program):
    response = test_app.get(f"/v1/clients/{program['client_uuid']}/programs/")
    assert response.status_code == 200
    program_obj = response.json()["items"][0]
    assert program_obj['uuid'] == program['uuid']
    assert program_obj['user_uuid'] == program['user_uuid']
    assert program_obj['client_uuid'] == program['client_uuid']

def test_integration_get_program(test_app, program):
    response = test_app.get(f"/v1/clients/{program['client_uuid']}/programs/{program['program_9char']}")
    assert response.status_code == 200
    program_obj = response.json()
    assert program_obj['program_9char'] == program['program_9char']
    assert program_obj['user_uuid'] == program['user_uuid']
    assert program_obj['client_uuid'] == program['client_uuid']

def test_integration_update_program(test_app, program):
    info_to_update = {
        "name": "updated",
        "description": "updated",
    }
    response = test_app.put(f"/v1/clients/{program['client_uuid']}/programs/{program['program_9char']}",  json=info_to_update)
    assert response.status_code == 200
    program_obj = response.json()
    assert program_obj['program_9char'] == program['program_9char']
    assert program_obj['user_uuid'] == program['user_uuid']
    assert program_obj['client_uuid'] == program['client_uuid']
    assert program_obj['name'] == "updated"
    assert program_obj['description'] == "updated"

def test_integration_delete_program(test_app, program):
    response = test_app.delete(f"/v1/clients/{program['client_uuid']}/programs/{program['program_9char']}")
    assert response.status_code == 200
    program_obj = response.json()
    assert program_obj['ok'] == True
    assert program_obj['Deleted']['program_9char'] == program['program_9char']
