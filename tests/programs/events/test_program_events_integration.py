from tests.testutil import new_program_event, update_program_event
from tests.conftest import is_deleted


def test_integration_get_program_events(test_app, program_with_updated_budget):
    program_events = test_app.get(f"/v1/clients/{program_with_updated_budget['client_uuid']}/programs/{program_with_updated_budget['program_9char']}/events")
    assert program_events.status_code == 200
    program_events = program_events.json()["items"]
    for event in program_events:
        try:
            assert event["client_uuid"] == program_with_updated_budget["client_uuid"]
            assert event["program_9char"] == program_with_updated_budget["program_9char"]
            assert event["program_uuid"] == program_with_updated_budget["uuid"]
            assert len(event["event_9char"]) == 9
        finally:
            deleted_program_event = test_app.delete(f"/v1/clients/{event['client_uuid']}/programs/{event['program_9char']}/delete_program_events/{event['event_9char']}")
            assert deleted_program_event.status_code == 200

def test_integration_get_program_event(test_app, program_with_updated_budget):
    program_events = test_app.get(f"/v1/clients/{program_with_updated_budget['client_uuid']}/programs/{program_with_updated_budget['program_9char']}/events").json()['items']
    single_event = program_events[0]
    program_event = test_app.get(f"/v1/clients/{program_with_updated_budget['client_uuid']}/programs/{program_with_updated_budget['program_9char']}/events/{single_event['event_9char']}")
    assert program_event.status_code == 200
    program_event = program_event.json()
    try:
        assert program_event["client_uuid"] == program_with_updated_budget["client_uuid"]
        assert program_event["program_9char"] == program_with_updated_budget["program_9char"]
        assert program_event["program_uuid"] == program_with_updated_budget["uuid"]
        assert len(program_event["event_9char"]) == 9
    finally:
        deleted_program_event = test_app.delete(f"/v1/clients/{program_event['client_uuid']}/programs/{program_event['program_9char']}/delete_program_events/{program_event['event_9char']}")
        assert deleted_program_event.status_code == 200


# event tests for client_awards, messages, program_messages, segment_messages
def test_integration_get_client_events(test_app, client_award):
    response = test_app.get(f"/v1/clients/{client_award['client_uuid']}/events")
    assert response.status_code == 200
    client_events = response.json()["items"]
    try:
        for event in client_events:
            assert event["client_uuid"] == client_award["client_uuid"]
            assert len(event["event_9char"]) == 9
    finally:
        deleted_client_events = test_app.delete(f"/v1/clients/{client_events[0]['client_uuid']}/delete_client_events")
        assert deleted_client_events.status_code == 200


def test_integration_delete_message_events(test_app, message,  program_message, segment_message):
    response = test_app.delete("/v1/delete_all_message_events")
    assert response.status_code == 200