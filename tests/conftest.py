import os
import pytest
import traceback
from fastapi.testclient import TestClient
import tests.testutil as util
from dotenv import load_dotenv
load_dotenv()

os.environ["TEST_MODE"] = "True"

from app.main import app


def err_msg(response):
    return f"Response[{response.status_code}]: {response.text} "


def delete_budget(test_app, budget):
    response = test_app.delete(f"/v1/clients/{budget['client_uuid']}/budgets/{budget['budget_9char']}")
    assert response.status_code == 200, err_msg(response)
    try:
        response = response.json()
        assert response["ok"] == True
        assert response["Deleted"]["uuid"] == budget["uuid"]
        assert response["Deleted"]["budget_9char"] == budget["budget_9char"]
    except TypeError:
        response = response[0]
        assert response["ok"] == True
        assert response["Deleted"]["uuid"] == budget["uuid"]
        assert response["Deleted"]["budget_9char"] == budget["budget_9char"]


def delete_user(test_app: TestClient, user_uuid: str, service_uuid: str):
    try:
        service_response = test_app.delete(f"/v1/users/{user_uuid}/services/{service_uuid}")
        user_response = test_app.delete(f"/v1/users/{user_uuid}")
        assert service_response.status_code == 200
        assert user_response.status_code == 200
        return
    except:
        if service_response.status_code == 200:
            assert service_response.status_code == 200
            assert user_response.status_code == 404
        elif user_response.status_code == 200:
            assert service_response.status_code == 404
            assert user_response.status_code == 200


def is_deleted(response):
    assert response.status_code == 200


@pytest.fixture(scope="module")
def test_app():
    try:
        client = TestClient(app)
        yield client
    finally:
        response = client.delete(f"/v1/delete_all_message_events")
        is_deleted(response)


@pytest.fixture(scope="module")
def user(test_app: TestClient):
    try:
        user = test_app.post("/v1/users?expand_services=true", json=util.new_user).json()
        yield user
    except:
        raise Exception("User Creation Failed")
    finally:
        if user is not None:
            delete_user(test_app, user["uuid"], user["services"]["email"][0]["uuid"])


@pytest.fixture(scope="module")
def service(user):
    yield user['services']['email'][0]


# FOR TESTING CLIENT ROUTES
@pytest.fixture(scope="module")
def client(test_app: TestClient):
    try:
        client = test_app.post(f"/v1/clients", json=util.single_client).json()
        yield client
    except:
        raise Exception("Client Creation Failed")
    finally:
        if client is not None:
            test_app.delete(f"/v1/clients/{client['uuid']}")


@pytest.fixture(scope="module")
def clients(test_app: TestClient):
    try:
        clients = test_app.post(f"/v1/clients", json=util.list_of_clients).json()
        yield clients
    except:
        raise Exception("Client Creation Failed")
    finally:
        for client in clients:
            if client is not None:
                test_app.delete(f"/v1/clients/{client['uuid']}")


@pytest.fixture(scope="module")
def client_user(test_app: TestClient, client):
    client_user = None
    try:
        client_user = test_app.post(
            f"/v1/clients/{client['uuid']}/users",
            json=util.new_client_user
        ).json()
        user = test_app.get(f"/v1/users/{client_user['user_uuid']}?expand_services=true")
        user = user.json()
        service_uuid = user["services"]["email"][0]["uuid"]
        yield client_user
    except Exception as e:
        print(f"Exception encountered: {e}")
        traceback.print_exc()
        raise e
    finally:
        if client_user is not None:
            test_app.delete(f"/v1/clients/{client['uuid']}/users/{client_user['uuid']}")
            test_app.delete(f"/v1/users/{user['uuid']}/services/{service_uuid}")
            test_app.delete(f"/v1/users/{user['uuid']}")


@pytest.fixture(scope="module")
def program(test_app: TestClient, client_user):
    try:
        util.new_program["user_uuid"] = client_user["user_uuid"]
        program = test_app.post(
            f"/v1/clients/{client_user['client_uuid']}/programs/",
            json=util.new_program
        ).json()
        yield program
    except Exception as e:
        print(f"Exception encountered: {e}")
        traceback.print_exc()
        raise e
    finally:
        if program is not None:
            test_app.delete(
                f"/v1/clients/{client_user['client_uuid']}/programs/{program['program_9char']}"
            )

@pytest.fixture(scope="module")
def program_admin(test_app: TestClient, program):
    try:
        util.new_program_admin['user_uuid'] = program['user_uuid']
        program_admin = test_app.post(
            f"/v1/clients/{program['client_uuid']}/programs/{program['program_9char']}/admins",
            json = util.new_program_admin
            ).json()
        yield program_admin
    except:
        raise Exception("Program Admin Creation Failed")
    finally:
        if program_admin is not None:
            test_app.delete(
                f"/v1/clients/{program_admin['client_uuid']}/programs/{program_admin['program_9char']}/admins/{program_admin['user_uuid']}"
            )


@pytest.fixture(scope="module")
def sub_event(test_app: TestClient, program_event):
    try:
        util.new_program_event["parent_9char"] = program_event["event_9char"]
        sub_event = test_app.post(
            f"/v1/clients/{program_event['client_uuid']}/programs/{program_event['program_9char']}/events",
            json = util.new_program_event
        ).json()
        yield sub_event
    except:
        raise Exception("Program Event Creation Failed")
    finally:
        if sub_event is not None:
            test_app.delete(
                f"/v1/clients/{sub_event['client_uuid']}/programs/{sub_event['program_9char']}/events/{sub_event['event_9char']}"
            )

@pytest.fixture(scope="module")
def program_rule(test_app: TestClient, program):
    try:
        program_rule = test_app.post(
            f"/v1/clients/{program['client_uuid']}/programs/{program['program_9char']}/rules",
            json=util.new_program_rule
        ).json()
        yield program_rule
    except:
        raise Exception("Program Rule Creation Failed")
    finally:
        if program_rule is not None:
            test_app.delete(
                f"/v1/clients/{program_rule['client_uuid']}/programs/{program_rule['program_9char']}/rules/{program_rule['rule_9char']}"
            )

@pytest.fixture(scope="module")
def segment(test_app: TestClient, program):
    try:
        program_segment = test_app.post(
            f"/v1/clients/{program['client_uuid']}/programs/{program['program_9char']}/segments",
            json=util.new_program_segment
        ).json()
        yield program_segment
    except:
        raise Exception("Program Segment Creation Failed")
    finally:
        if program_segment is not None:
            test_app.delete(
                f"/v1/clients/{program_segment['client_uuid']}/programs/{program_segment['program_9char']}/segments/{program_segment['segment_9char']}"
            )

@pytest.fixture(scope="module")
def segment_rule(test_app: TestClient, segment):
    try:
        segment_rule = test_app.post(
            f"/v1/clients/{segment['client_uuid']}/programs/{segment['program_9char']}/segments/{segment['segment_9char']}/rules",
            json=util.new_segment_rule
        ).json()
        yield segment_rule
    except:
        raise Exception("Segment Rule Creation Failed")
    finally:
        if segment_rule is not None:
            test_app.delete(
                f"/v1/clients/{segment_rule['client_uuid']}/programs/{segment_rule['program_9char']}/segments/{segment_rule['segment_9char']}/rules/{segment_rule['rule_9char']}"
            )

@pytest.fixture(scope="module")
def segment_design(test_app: TestClient, segment):
    try:
        segment_design = test_app.post(
            f"/v1/clients/{segment['client_uuid']}/programs/{segment['program_9char']}/segments/{segment['segment_9char']}/designs",
            json=util.new_segment_design
        ).json()
        yield segment_design
    except:
        raise Exception("Segment design Creation Failed")
    finally:
        if segment_design is not None:
            test_app.delete(
                f"/v1/clients/{segment_design['client_uuid']}/programs/{segment_design['program_9char']}/segments/{segment_design['segment_9char']}/designs/{segment_design['design_9char']}"
            )

@pytest.fixture(scope="module")
def award(test_app: TestClient):
    try:
        award = test_app.post(f"/v1/awards", json=util.new_award).json()
        yield award
    except:
        raise Exception("Award Creation Failed")
    finally:
        if award is not None:
            test_app.delete(f"/v1/awards/{award['uuid']}")

@pytest.fixture(scope="module")
def client_award(test_app: TestClient, client):
    try:
        client_award = test_app.post(
            f"/v1/clients/{client['uuid']}/awards",
            json=util.new_client_award
        ).json()
        yield client_award
    except:
        raise Exception("Client Award Creation Failed")
    finally:
        if client_award is not None:
            test_app.delete(
                f"/v1/clients/{client_award['client_uuid']}/awards/{client_award['client_award_9char']}"
            )

@pytest.fixture(scope="module")
def program_award(test_app: TestClient, program, client_award):
    try:
        program_award = test_app.post(
            f"/v1/clients/{program['client_uuid']}/programs/{program['program_9char']}/awards/{client_award['client_award_9char']}",
            json=util.new_program_award
        ).json()
        yield program_award
    except:
        raise Exception("Program Award Creation Failed")
    finally:
        if program_award is not None:
            test_app.delete(
                f"/v1/clients/{program_award['client_uuid']}/programs/{program_award['program_9char']}/awards/{program_award['program_award_9char']}"
            )

@pytest.fixture(scope="module")
def segment_award(test_app: TestClient, segment, program_award):
    try:
        util.new_segment_award["client_award_9char"] = program_award["client_award_9char"]
        segment_award = test_app.post(
            f"/v1/clients/{program_award['client_uuid']}/programs/{program_award['program_9char']}/segments/{segment['segment_9char']}/awards/{program_award['program_award_9char']}",
            json=util.new_segment_award
        ).json()
        yield segment_award
    except:
        raise Exception("Program Award Creation Failed")
    finally:
        if segment_award is not None:
            test_app.delete(
                f"/v1/clients/{segment_award['client_uuid']}/programs/{segment_award['program_9char']}/segments/{segment_award['segment_9char']}/awards/{segment_award['segment_award_9char']}"
            )


@pytest.fixture(scope="function")
def static_budget(test_app: TestClient, client):
    try:
        static_budget = test_app.post(f"/v1/clients/{client['uuid']}/budgets", json=util.new_static_budget).json()
        yield static_budget
    except:
        raise Exception("client static budget Creation Failed")
    finally:
        if static_budget is not None:
            delete_budget(test_app, static_budget)


@pytest.fixture(scope="function")
def parent_static_budget(test_app: TestClient, static_budget):
    try:
        util.new_parent_static_budget["parent_9char"] = static_budget["budget_9char"]
        parent_static_budget = test_app.post(f"/v1/clients/{static_budget['client_uuid']}/budgets", json=util.new_parent_static_budget).json()
        yield parent_static_budget
    except:
        raise Exception("client Parent Budget Creation Failed")
    finally:
        if parent_static_budget is not None:
            delete_budget(test_app, parent_static_budget)


@pytest.fixture(scope="function")
def parent_budget_no_cap(test_app: TestClient, static_budget):
    try:
        util.new_parent_budget_no_cap["parent_9char"] = static_budget["budget_9char"]
        parent_budget_no_cap = test_app.post(f"/v1/clients/{static_budget['client_uuid']}/budgets", json=util.new_parent_budget_no_cap).json()
        yield parent_budget_no_cap
    except:
        raise Exception("client Sub Budget Creation Failed")
    finally:
        if parent_budget_no_cap is not None:
            delete_budget(test_app, parent_budget_no_cap)


@pytest.fixture(scope="function")
def parent_budget_cap(test_app: TestClient, static_budget):
    try:
        util.new_parent_budget_cap["parent_9char"] = static_budget["budget_9char"]
        parent_budget_cap = test_app.post(f"/v1/clients/{static_budget['client_uuid']}/budgets", json=util.new_parent_budget_cap).json()
        yield parent_budget_cap
    except:
        raise Exception("client Sub Budget Creation Failed")
    finally:
        if parent_budget_cap is not None:
            delete_budget(test_app, parent_budget_cap)


@pytest.fixture(scope="function")
def sub_budget_cap_from_parent_with_cap(test_app: TestClient, parent_budget_cap):
    try:
        util.new_sub_budget_cap["parent_9char"] = parent_budget_cap["budget_9char"]
        sub_budget_cap = test_app.post(f"/v1/clients/{parent_budget_cap['client_uuid']}/budgets", json=util.new_sub_budget_cap).json()
        yield sub_budget_cap
    except:
        raise Exception("Client Sub Budget Creation Failed")
    finally:
        if sub_budget_cap is not None:
            delete_budget(test_app, sub_budget_cap)


@pytest.fixture(scope="function")
def sub_budget_cap_from_parent_no_cap(test_app: TestClient, parent_budget_no_cap):
    try:
        util.new_sub_budget_cap["parent_9char"] = parent_budget_no_cap["budget_9char"]
        sub_budget_cap = test_app.post(f"/v1/clients/{parent_budget_no_cap['client_uuid']}/budgets", json=util.new_sub_budget_cap).json()
        yield sub_budget_cap
    except:
        raise Exception("Client Sub Budget Creation Failed")
    finally:
        if sub_budget_cap is not None:
            delete_budget(test_app, sub_budget_cap)


@pytest.fixture(scope="function")
def sub_budget_no_cap_from_parent_with_cap(test_app: TestClient, parent_budget_cap):
    try:
        util.new_sub_budget_no_cap["parent_9char"] = parent_budget_cap["budget_9char"]
        sub_budget_no_cap = test_app.post(f"/v1/clients/{parent_budget_cap['client_uuid']}/budgets", json=util.new_sub_budget_no_cap).json()
        yield sub_budget_no_cap
    except:
        raise Exception("Client Sub Budget Creation Failed")
    finally:
        if sub_budget_no_cap is not None:
            delete_budget(test_app, sub_budget_no_cap)


@pytest.fixture(scope="function")
def sub_budget_no_cap_from_parent_no_cap(test_app: TestClient, parent_budget_no_cap):
    try:
        util.new_sub_budget_no_cap["parent_9char"] = parent_budget_no_cap["budget_9char"]
        sub_budget_no_cap = test_app.post(f"/v1/clients/{parent_budget_no_cap['client_uuid']}/budgets", json=util.new_sub_budget_no_cap).json()
        yield sub_budget_no_cap
    except:
        raise Exception("Client Sub Budget Creation Failed")
    finally:
        if sub_budget_no_cap is not None:
            delete_budget(test_app, sub_budget_no_cap)


@pytest.fixture(scope="function")
def message(test_app: TestClient):
    try:
        message = test_app.post(f"/v1/messages",  json=util.new_message).json()
        yield message
    except:
        raise Exception("Message Creation Failed")
    finally:
        if message is not None:
            response = test_app.delete(f"/v1/messages/{message['message_9char']}")
            is_deleted(response)


@pytest.fixture(scope="function")
def client_message(test_app: TestClient):
    try:
        message = test_app.post(f"/v1/messages",  json=util.new_client_message).json()
        yield message
    except:
        raise Exception("Client Message Creation Failed")
    finally:
        if message is not None:
            response = test_app.delete(f"/v1/messages/{message['message_9char']}")
            is_deleted(response)


@pytest.fixture(scope="function")
def program_message(test_app, program):
    try:
        program_message = test_app.post(f"/v1/clients/{program['client_uuid']}/programs/{program['program_9char']}/messages",  json=util.new_program_message).json()
        yield program_message
    except:
        raise Exception("program_message Creation Failed")
    finally:
        if program_message is not None:
            response = test_app.delete(f"/v1/messages/{program_message['message_9char']}")
            is_deleted(response)


@pytest.fixture(scope="function")
def segment_message(test_app, segment):
    try:
        segment_message = test_app.post(f"/v1/clients/{segment['client_uuid']}/programs/{segment['program_9char']}/segments/{segment['segment_9char']}/messages",  json=util.new_segment_message).json()
        yield segment_message
    except:
        raise Exception("segment_message Creation Failed")
    finally:
        if segment_message is not None:
            response = test_app.delete(f"/v1/messages/{segment_message['message_9char']}")
            is_deleted(response)


@pytest.fixture(scope="function")
def program_with_updated_budget(test_app, client_user, static_budget):
    try:
        util.new_program["budget_9char"] = static_budget["budget_9char"]
        util.new_program["user_uuid"] = client_user["user_uuid"]
        program_with_updated_budget = test_app.post(f"/v1/clients/{static_budget['client_uuid']}/programs/", json=util.new_program).json()
        # updating budget triggers an event that shows the connection of the budget with program
        updated_budget = test_app.put(f"/v1/clients/{program_with_updated_budget['client_uuid']}/budgets/{program_with_updated_budget['budget_9char']}", json=util.update_static_budget).json()
        yield program_with_updated_budget
    except:
        raise Exception("Program with updated budget creation failed")
    finally:
        if program_with_updated_budget is not None:
            deleted_program = test_app.delete(f"/v1/clients/{program_with_updated_budget['client_uuid']}/programs/{program_with_updated_budget['program_9char']}")
            is_deleted(deleted_program)
