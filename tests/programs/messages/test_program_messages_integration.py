from tests.testutil import new_program_message, update_message


def test_integration_create_program_message(program_message):
    assert "uuid" in program_message
    assert len(program_message["message_9char"]) == 9
    assert program_message["name"] == new_program_message["name"]
    assert program_message["body"] == new_program_message["body"]


def test_integration_get_program_messages(test_app, program_message):
    response = test_app.get(f"/v1/clients/{program_message['client_uuid']}/programs/{program_message['program_9char']}/messages")
    assert response.status_code == 200
    response = response.json()["items"]
    for item in response:
        assert ["uuid", "name", "body"] is not None
        assert len(item["message_9char"]) == 9


def test_integration_get_program_message(test_app, program_message):
    response = test_app.get(f"/v1/clients/{program_message['client_uuid']}/programs/{program_message['program_9char']}/messages/{program_message['message_9char']}")
    assert response.status_code == 200
    response = response.json()
    assert response["uuid"] == program_message["uuid"]
    assert response["message_9char"] == program_message["message_9char"]
    assert response["name"] == program_message["name"]
    assert response["body"] == program_message["body"]


def test_integration_update_program_message(test_app, program_message):
    response = test_app.put(f"/v1/clients/{program_message['client_uuid']}/programs/{program_message['program_9char']}/messages/{program_message['message_9char']}", json=update_message)
    assert response.status_code == 200
    response = response.json()
    assert response["uuid"] == program_message["uuid"]
    assert response["message_9char"] == program_message["message_9char"]
    assert response["name"] == update_message["name"]
    assert response["body"] == update_message["body"]


def test_integration_delete_program_message(test_app, program):
    try:
        message = test_app.post(f"/v1/clients/{program['client_uuid']}/programs/{program['program_9char']}/messages",  json=new_program_message).json()
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

