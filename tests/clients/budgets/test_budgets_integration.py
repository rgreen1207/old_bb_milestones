import tests.testutil as util


def test_create_static_budget(client, static_budget):
    assert "uuid" in static_budget
    assert client["uuid"] == static_budget["client_uuid"]
    assert "budget_9char" in static_budget
    assert static_budget["budget_type"] == "static"

# test creation of static parent from static budget, and that the static value is removed from it's parent.
def test_create_parent_static_budget_from_static(test_app, client, parent_static_budget):
    static_budget = test_app.get(f"/v1/clients/{parent_static_budget['client_uuid']}/budgets/{parent_static_budget['parent_9char']}")
    static_budget = static_budget.json()
    assert "uuid" in parent_static_budget
    assert client["uuid"] == parent_static_budget["client_uuid"]
    assert static_budget["budget_9char"] == parent_static_budget["parent_9char"]
    assert parent_static_budget["budget_type"] == "static"
    assert parent_static_budget["value"] == util.new_parent_static_budget["value"]
    assert static_budget["value"] == util.new_static_budget["value"] - parent_static_budget["value"]


def test_create_parent_budget_no_cap_from_static(client, static_budget, parent_budget_no_cap):
    assert "uuid" in parent_budget_no_cap
    assert client["uuid"] == parent_budget_no_cap["client_uuid"]
    assert static_budget["budget_9char"] == parent_budget_no_cap["parent_9char"]
    assert parent_budget_no_cap["budget_type"] == "passthru_nocap"


def test_create_parent_budget_cap_from_static(client, static_budget, parent_budget_cap):
    assert "uuid" in parent_budget_cap
    assert client["uuid"] == parent_budget_cap["client_uuid"]
    assert static_budget["budget_9char"] == parent_budget_cap["parent_9char"]
    assert parent_budget_cap["budget_type"] == "passthru_cap"


def test_create_sub_budget_no_cap_from_parent_with_cap(parent_budget_cap, sub_budget_no_cap_from_parent_with_cap):
    sub_budget_no_cap = sub_budget_no_cap_from_parent_with_cap
    assert sub_budget_no_cap["parent_9char"] == parent_budget_cap["budget_9char"]
    assert sub_budget_no_cap["budget_type"] == "passthru_nocap"


def test_create_sub_budget_cap_from_parent_with_cap(parent_budget_cap, sub_budget_cap_from_parent_with_cap):
    sub_budget_cap = sub_budget_cap_from_parent_with_cap
    assert sub_budget_cap["parent_9char"] == parent_budget_cap["budget_9char"]
    assert sub_budget_cap["budget_type"] == "passthru_cap"


def test_create_sub_budget_no_cap_from_parent_with_no_cap(parent_budget_no_cap, sub_budget_no_cap_from_parent_no_cap):
    sub_budget_no_cap = sub_budget_no_cap_from_parent_no_cap
    assert sub_budget_no_cap["parent_9char"] == parent_budget_no_cap["budget_9char"]
    assert sub_budget_no_cap["budget_type"] == "passthru_nocap"


def test_create_sub_budget_with_cap_from_parent_with_no_cap(parent_budget_no_cap, sub_budget_cap_from_parent_no_cap):
    sub_budget_cap = sub_budget_cap_from_parent_no_cap
    assert sub_budget_cap["parent_9char"] == parent_budget_no_cap["budget_9char"]
    assert sub_budget_cap["budget_type"] == "passthru_cap"


def test_create_static_budget_from_parent_with_cap(test_app, parent_budget_cap):
    util.new_sub_static_budget["parent_9char"] = parent_budget_cap["budget_9char"]
    sub_static_budget = test_app.post(f"/v1/clients/{parent_budget_cap['client_uuid']}/budgets",  json=util.new_sub_static_budget)
    try:
        assert sub_static_budget.status_code == 405
        sub_static_budget = sub_static_budget.json()
        assert "detail" in sub_static_budget
    finally:
        if "detail" not in sub_static_budget:
            test_app.delete(f"/v1/clients/{sub_static_budget['client_uuid']}/budgets/{sub_static_budget['budget_9char']}")


def test_create_static_budget_from_parent_with_no_cap(test_app, parent_budget_no_cap):
    util.new_sub_static_budget["parent_9char"] = parent_budget_no_cap["budget_9char"]
    sub_static_budget = test_app.post(f"/v1/clients/{parent_budget_no_cap['client_uuid']}/budgets",  json=util.new_sub_static_budget)
    try:
        assert sub_static_budget.status_code == 405
        sub_static_budget = sub_static_budget.json()
        assert "detail" in sub_static_budget
    finally:
        if "detail" not in sub_static_budget:
            test_app.delete(f"/v1/clients/{sub_static_budget['client_uuid']}/budgets/{sub_static_budget['budget_9char']}")


# this tests that when an update request is sent to an un-capped budget with a new value that it will pass it through to the static parent
def test_update_value_parent_budget_no_cap_from_static_parent(test_app, static_budget, parent_budget_no_cap):
    value = 500
    updated_budgets = test_app.put(f"/v1/clients/{parent_budget_no_cap['client_uuid']}/budgets/{parent_budget_no_cap['budget_9char']}",  json={"value": value})
    updated_budgets = updated_budgets.json()
    assert updated_budgets["updated"]["value"] == 0
    assert updated_budgets["updated"]["budget_type"] == 1
    assert updated_budgets["static_parent"]["value"] == static_budget["value"] - value


# this tests that when an update request is sent to a capped budget with a new value that it will deduct it from the budgets cap and also from the parent
def test_update_value_parent_budget_with_cap_from_static_parent(test_app, static_budget, parent_budget_cap):
    value = 500
    updated_budgets = test_app.put(f"/v1/clients/{parent_budget_cap['client_uuid']}/budgets/{parent_budget_cap['budget_9char']}",  json={"value": value})
    updated_budgets = updated_budgets.json()
    assert updated_budgets["updated"]["value"] == parent_budget_cap["value"] + value
    assert updated_budgets["updated"]["budget_type"] == 2
    assert updated_budgets["static_parent"]["value"] == static_budget["value"] - value


def test_update_value_sub_budget_no_cap_from_parent_no_cap(test_app, static_budget, sub_budget_no_cap_from_parent_no_cap):
    value = 500
    sub_budget = sub_budget_no_cap_from_parent_no_cap
    updated_budgets = test_app.put(f"/v1/clients/{sub_budget['client_uuid']}/budgets/{sub_budget['budget_9char']}",  json={"value": value})
    updated_budgets = updated_budgets.json()
    assert updated_budgets["updated"]["value"] == 0
    assert updated_budgets["updated"]["budget_type"] == 1
    assert updated_budgets["static_parent"]["value"] == static_budget["value"] - value


def test_update_value_sub_budget_with_cap_from_parent_no_cap(test_app, static_budget, sub_budget_cap_from_parent_no_cap):
    value = 500
    sub_budget = sub_budget_cap_from_parent_no_cap
    updated_budgets = test_app.put(f"/v1/clients/{sub_budget['client_uuid']}/budgets/{sub_budget['budget_9char']}",  json={"value": value})
    updated_budgets = updated_budgets.json()
    assert updated_budgets["updated"]["value"] == sub_budget["value"] + value
    assert updated_budgets["updated"]["budget_type"] == 2
    assert updated_budgets["static_parent"]["value"] == static_budget["value"] - value


def test_integration_get_budgets(test_app, static_budget):
    response = test_app.get(f"/v1/clients/{static_budget['client_uuid']}/budgets")
    assert response.status_code == 200
    response = response.json()["items"][0]
    assert response['client_uuid'] == static_budget['client_uuid']
    assert response['uuid'] == static_budget['uuid']


def test_integration_get_budget(test_app, static_budget):
    response = test_app.get(f"/v1/clients/{static_budget['client_uuid']}/budgets/{static_budget['budget_9char']}")
    assert response.status_code == 200
    response = response.json()
    assert "uuid" in response
    assert response["client_uuid"] == static_budget["client_uuid"]
    assert response["budget_9char"] == static_budget["budget_9char"]


def test_integration_update_budget(test_app, static_budget):
    response = test_app.put(f"/v1/clients/{static_budget['client_uuid']}/budgets/{static_budget['budget_9char']}", json=util.update_static_budget)
    assert response.status_code == 200
    response = response.json()
    assert response["client_uuid"] == static_budget["client_uuid"]
    assert response["uuid"] == static_budget["uuid"]
    assert response["budget_9char"] == static_budget["budget_9char"]
    assert response["name"] == util.update_static_budget["name"]


def test_integration_delete_budget(test_app, client):
    budget = test_app.post(f"/v1/clients/{client['uuid']}/budgets", json=util.new_static_budget)
    budget = budget.json()
    try:
        assert budget["client_uuid"] == client["uuid"]
        response = test_app.delete(f"/v1/clients/{client['uuid']}/budgets/{budget['budget_9char']}")
        assert response.status_code == 200
        response = response.json()
        assert response["ok"] == True
        assert response["Deleted"]["uuid"] == budget["uuid"]
        assert response["Deleted"]["budget_9char"] == budget["budget_9char"]
    finally:
        test_app.delete(f"/v1/clients/{client['uuid']}/budgets/{budget['budget_9char']}")
