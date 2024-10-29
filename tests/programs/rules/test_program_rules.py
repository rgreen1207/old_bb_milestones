from fastapi.testclient import TestClient
import tests.testutil as utils


def test_get_all_program_rules(test_app: TestClient, program_rule: dict):
    response = test_app.get(
        f"/v1/clients/{program_rule['client_uuid']}/programs/{program_rule['program_9char']}/rules"
    )
    assert response.status_code == 200
    assert response.json()["items"][0]["status"] == program_rule["status"]


def test_get_program_rule(test_app: TestClient, program_rule: dict):
    response = test_app.get(
        f"/v1/clients/{program_rule['client_uuid']}/programs/{program_rule['program_9char']}/rules/{program_rule['rule_9char']}"
    )
    assert response.status_code == 200
    assert response.json()["status"] == program_rule["status"]


def test_create_program_rule(program_rule: dict):
    assert "uuid" in program_rule
    assert program_rule["status"] == "published"


def test_update_program_rule(test_app: TestClient, program_rule: dict):
    response = test_app.put(
        f"/v1/clients/{program_rule['client_uuid']}/programs/{program_rule['program_9char']}/rules/{program_rule['rule_9char']}",
        json = utils.update_program_rule
    )
    assert response.status_code == 200
    assert response.json()["status"] == "draft"


def test_delete_program_rule(test_app: TestClient, program_rule: dict):
    response = test_app.delete(
        f"/v1/clients/{program_rule['client_uuid']}/programs/{program_rule['program_9char']}/rules/{program_rule['rule_9char']}"
    )
    assert response.status_code == 200
    assert response.json()["ok"] == True
