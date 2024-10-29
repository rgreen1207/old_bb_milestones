from tests.testutil import new_segment_rule, update_segment_rule


def test_get_all_segments_rules(test_app, segment_rule):
    response = test_app.get(f"/v1/clients/{segment_rule['client_uuid']}/programs/{segment_rule['program_9char']}/segments/{segment_rule['segment_9char']}/rules")
    assert response.status_code == 200
    response = response.json()["items"][0]
    assert response["client_uuid"] == segment_rule["client_uuid"]
    assert response["program_9char"] == segment_rule["program_9char"]
    assert response["segment_9char"] == segment_rule["segment_9char"]
    assert response["rule_9char"] == segment_rule["rule_9char"]
    assert response["program_uuid"] == segment_rule["program_uuid"]
    assert response["rule_type"] == segment_rule["rule_type"]
    assert response["status"] == segment_rule["status"]
    assert response["logic"] == segment_rule["logic"]

def test_get_segment_rule(test_app, segment_rule):
    response = test_app.get(f"/v1/clients/{segment_rule['client_uuid']}/programs/{segment_rule['program_9char']}/segments/{segment_rule['segment_9char']}/rules/{segment_rule['rule_9char']}")
    assert response.status_code == 200
    response = response.json()
    assert response["client_uuid"] == segment_rule["client_uuid"]
    assert response["program_9char"] == segment_rule["program_9char"]
    assert response["segment_9char"] == segment_rule["segment_9char"]
    assert response["rule_9char"] == segment_rule["rule_9char"]
    assert response["program_uuid"] == segment_rule["program_uuid"]
    assert response["rule_type"] == segment_rule["rule_type"]
    assert response["status"] == segment_rule["status"]
    assert response["logic"] == segment_rule["logic"]

def test_create_segment_rule(segment_rule):
    keys = ["program_uuid", "client_uuid", "program_9char", "segment_9char", "rule_9char"]
    for key in keys:
        assert key in segment_rule
    assert len(segment_rule["rule_9char"]) == 9
    assert segment_rule["rule_type"] == new_segment_rule["rule_type"]
    assert segment_rule["status"] == new_segment_rule["status"]
    assert segment_rule["logic"] == new_segment_rule["logic"]

def test_update_segment_rule(test_app, segment_rule):
    response = test_app.put(f"/v1/clients/{segment_rule['client_uuid']}/programs/{segment_rule['program_9char']}/segments/{segment_rule['segment_9char']}/rules/{segment_rule['rule_9char']}",  json=update_segment_rule)
    assert response.status_code == 200
    response = response.json()
    assert response["client_uuid"] == segment_rule["client_uuid"]
    assert response["program_9char"] == segment_rule["program_9char"]
    assert response["segment_9char"] == segment_rule["segment_9char"]
    assert response["rule_9char"] == segment_rule["rule_9char"]
    assert response["program_uuid"] == segment_rule["program_uuid"]
    assert response["rule_type"] == update_segment_rule["rule_type"]
    assert response["status"] == update_segment_rule["status"]
    assert response["logic"] == update_segment_rule["logic"]

def test_delete_segment_rule(test_app, segment_rule):
    response = test_app.delete(f"/v1/clients/{segment_rule['client_uuid']}/programs/{segment_rule['program_9char']}/segments/{segment_rule['segment_9char']}/rules/{segment_rule['rule_9char']}")
    assert response.status_code == 200
    response_ok = response.json()["ok"]
    response_deleted = response.json()["Deleted"]
    assert response_ok == True
    assert response_deleted["uuid"] == segment_rule["uuid"]

