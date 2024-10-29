from tests.testutil import new_message, update_message


def test_integration_create_message(message):
    assert "uuid" in message
    assert len(message["message_9char"]) == 9
    assert message["name"] == new_message["name"]
    assert message["body"] == new_message["body"]

def test_integration_get_messages(test_app, message):
    response = test_app.get(f"/v1/messages")
    assert response.status_code == 200
    response = response.json()["items"]
    for item in response:
        assert ["uuid", "name", "body"] is not None
        assert len(item["message_9char"]) == 9

def test_integration_get_all_client_messages(test_app, client_message):
    response = test_app.get(f"/v1/messages/client/{client_message['client_uuid']}")
    assert response.status_code == 200
    response = response.json()["items"]
    for item in response:
        assert ["uuid", "name", "body"] is not None
        assert len(item["message_9char"]) == 9
        assert item['client_uuid'] == client_message['client_uuid']

def test_integration_get_message(test_app, message):
    response = test_app.get(f"/v1/messages/{message['message_9char']}")
    assert response.status_code == 200
    response = response.json()
    assert response["uuid"] == message["uuid"]
    assert response["message_9char"] == message["message_9char"]
    assert response["name"] == message["name"]
    assert response["body"] == message["body"]

def test_integration_update_message(test_app, message):
    response = test_app.put(f"/v1/messages/{message['message_9char']}", json=update_message)
    assert response.status_code == 200
    response = response.json()
    assert response["uuid"] == message["uuid"]
    assert response["message_9char"] == message["message_9char"]
    assert response["name"] == update_message["name"]
    assert response["body"] == update_message["body"]

def test_integration_delete_message(test_app):
    try:
        message = test_app.post(f"/v1/messages",  json=new_message).json()
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

