from tests.testutil import new_segment_design, update_segment_design


def test_get_all_segments_designs(test_app, segment_design):
    response = test_app.get(f"/v1/clients/{segment_design['client_uuid']}/programs/{segment_design['program_9char']}/segments/{segment_design['segment_9char']}/designs")
    assert response.status_code == 200
    response = response.json()["items"][0]
    assert response["client_uuid"] == segment_design["client_uuid"]
    assert response["program_9char"] == segment_design["program_9char"]
    assert response["segment_9char"] == segment_design["segment_9char"]
    assert response["design_9char"] == segment_design["design_9char"]
    assert response["program_uuid"] == segment_design["program_uuid"]
    assert response["channel"] == segment_design["channel"]
    assert response["status"] == "draft"
    assert response["message_uuid"] == segment_design["message_uuid"]

def test_get_segment_design(test_app, segment_design):
    response = test_app.get(f"/v1/clients/{segment_design['client_uuid']}/programs/{segment_design['program_9char']}/segments/{segment_design['segment_9char']}/designs/{segment_design['design_9char']}")
    assert response.status_code == 200
    response = response.json()
    assert response["client_uuid"] == segment_design["client_uuid"]
    assert response["program_9char"] == segment_design["program_9char"]
    assert response["segment_9char"] == segment_design["segment_9char"]
    assert response["design_9char"] == segment_design["design_9char"]
    assert response["program_uuid"] == segment_design["program_uuid"]
    assert response["channel"] == segment_design["channel"]
    assert response["status"] == segment_design["status"]
    assert response["message_uuid"] == segment_design["message_uuid"]

def test_create_segment_design(segment_design):
    keys = ["program_uuid", "client_uuid", "program_9char", "segment_9char", "design_9char"]
    for key in keys:
        assert key in segment_design
    assert len(segment_design["design_9char"]) == 9
    assert segment_design["channel"] == new_segment_design["channel"]
    assert segment_design["status"] == "draft"
    assert segment_design["message_uuid"] == new_segment_design["message_uuid"]

def test_update_segment_design(test_app, segment_design):
    response = test_app.put(f"/v1/clients/{segment_design['client_uuid']}/programs/{segment_design['program_9char']}/segments/{segment_design['segment_9char']}/designs/{segment_design['design_9char']}",  json=update_segment_design)
    assert response.status_code == 200
    response = response.json()
    assert response["client_uuid"] == segment_design["client_uuid"]
    assert response["program_9char"] == segment_design["program_9char"]
    assert response["segment_9char"] == segment_design["segment_9char"]
    assert response["design_9char"] == segment_design["design_9char"]
    assert response["program_uuid"] == segment_design["program_uuid"]
    assert response["channel"] == update_segment_design["channel"]
    assert response["status"] == "disabled"

def test_delete_segment_design(test_app, segment_design):
    response = test_app.delete(f"/v1/clients/{segment_design['client_uuid']}/programs/{segment_design['program_9char']}/segments/{segment_design['segment_9char']}/designs/{segment_design['design_9char']}")
    assert response.status_code == 200
    response_ok = response.json()["ok"]
    response_deleted = response.json()["Deleted"]
    assert response_ok == True
    keys = ["program_uuid", "client_uuid", "program_9char", "segment_9char", "design_9char"]
    for key in keys:
        assert response_deleted[key] == segment_design[key]
