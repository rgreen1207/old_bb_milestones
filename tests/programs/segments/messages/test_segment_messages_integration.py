from tests.testutil import new_segment_message, update_message


def test_integration_create_segment_message(segment_message):
    assert "uuid" in segment_message
    assert len(segment_message["message_9char"]) == 9
    assert segment_message["name"] == new_segment_message["name"]
    assert segment_message["body"] == new_segment_message["body"]


def test_integration_get_segment_messages(test_app, segment_message):
    response = test_app.get(f"/v1/clients/{segment_message['client_uuid']}/programs/{segment_message['program_9char']}/segments/{segment_message['segment_9char']}/messages")
    assert response.status_code == 200
    response = response.json()["items"]
    for item in response:
        assert ["uuid", "name", "body"] is not None
        assert len(item["message_9char"]) == 9


def test_integration_get_segment_message(test_app, segment_message):
    response = test_app.get(f"/v1/clients/{segment_message['client_uuid']}/programs/{segment_message['program_9char']}/segments/{segment_message['segment_9char']}/messages/{segment_message['message_9char']}")
    assert response.status_code == 200
    response = response.json()
    assert response["uuid"] == segment_message["uuid"]
    assert response["message_9char"] == segment_message["message_9char"]
    assert response["name"] == segment_message["name"]
    assert response["body"] == segment_message["body"]


def test_integration_update_segment_message(test_app, segment_message):
    response = test_app.put(f"/v1/clients/{segment_message['client_uuid']}/programs/{segment_message['program_9char']}/segments/{segment_message['segment_9char']}/messages/{segment_message['message_9char']}", json=update_message)
    assert response.status_code == 200
    response = response.json()
    assert response["uuid"] == segment_message["uuid"]
    assert response["message_9char"] == segment_message["message_9char"]
    assert response["name"] == update_message["name"]
    assert response["body"] == update_message["body"]


def test_integration_delete_segment_message(test_app, segment):
    try:
        message = test_app.post(f"/v1/clients/{segment['client_uuid']}/programs/{segment['program_9char']}/segments/{segment['segment_9char']}/messages",  json=new_segment_message).json()
        if message is not None:
            response = test_app.delete(f"/v1/messages/{message['message_9char']}").json()
            assert response["ok"] == True
            assert response["Deleted"]["uuid"] == message["uuid"]
            assert response["Deleted"]["message_9char"] == message["message_9char"]
            if response["Deleted"]["client_uuid"] is not None:
                assert response["Deleted"]["status"] is not 2
    except:
        raise Exception("Message Creation Failed")
    finally:
        response = test_app.delete(f"/v1/messages/{message['message_9char']}").json()
