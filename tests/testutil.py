from collections import namedtuple
from app.utilities import SHA224Hash


uuid_names = [
    "user_uuid",
    "first_client_uuid",
    "second_client_uuid",
    "client_user_uuid",
    "program_uuid",
    "award_uuid"
]
Test_IDs = namedtuple("Test_ID", uuid_names)
test_uuids = Test_IDs(*[SHA224Hash() for _ in uuid_names])

new_user = {
    "uuid": test_uuids.user_uuid,
    "client_uuid": test_uuids.first_client_uuid,
    "first_name": "Test",
    "last_name": "User",
    "work_email": "test.user123@testclient.com",
    "cell_number": "(579)741-2145",
    "hire_date": "1/1/2015",
    "continuous_service_date": "1/1/2015",
    "employee_id": 1139,
    "manager_id": 200405,
    "cost_center_id": 21121,
    "worker_type": "Employee",
    "department": "Engineering",
    "manager": "Jason W",
    "location": "Seattle",
    "business_title": "Blueboard Engineer",
    "department_leader": 200405
}

update_user = {
    "first_name": "Test_Update",
    "last_name": "User_Update",
    "latidude": 33812263,
    "longitude": -117920126,
    # "time_birdthday": 1420070400,
    "admin": 1
}

new_service = {
    "service_uuid": "email",
    "service_user_id": "test.user2@testclient.com"
}

update_service = {
    "service_user_screenname": "test",
    "service_user_name": "test",
    "service_access_token": "test",
    "service_access_secret": "test",
    "service_refresh_token": "test",
    # "service_uuid": "test"
}

single_client = {
    "uuid":test_uuids.first_client_uuid,
    "name": "test",
    "description": "test",
    "status": 0
}

list_of_clients = [
    {
    "uuid": test_uuids.first_client_uuid,
    "name": "client one",
    "description": "first client",
    "status": 0
    },
    {
    "uuid": test_uuids.second_client_uuid,
    "name": "client two",
    "description": "second client",
    "status": 0
    }
]
new_client_user = {
    "uuid": test_uuids.client_user_uuid,
    "client_uuid": test_uuids.first_client_uuid,
    "email_address": "test.user123@testclient.com",
    "first_name": "Test",
    "last_name": "User",
    "admin": 1
}

update_client_user = {
    "title": "test",
    "department": "test"
}

new_program = {
    "uuid": test_uuids.program_uuid,
    "user_uuid": None,
    "name": "Pytest Blueboard 2023 Anniversary Program",
    "description": "This program sends rewards to Blueboard employees on the Anniversary of their start date at the Company.",
    "budget_9char": "budg_9cha",
    "status": 1,
    "program_type": 4,
    "cadence": 1,
    "cadence_value": 2
}

new_program_admin = {
    "program_uuid": test_uuids.program_uuid,
    "user_uuid": None,
    "permissions": 2
}

update_program_admin = {
    "permissions": 1
}

new_program_event = {
    "event_type": 1,
    "parent_9char": None,
    "event_data": "pytest-event",
    "status": 1
}

update_program_event = {
    "event_type": 2,
    "event_data": "pytest-updated-event",
    "status": 2
}

new_program_segment = {
    "budget_9char": None,
    "name": "pytest segment",
    "description": "this is a segment",
    "status": 2
}

update_program_segment = {
    "name": "pytest updated segment",
    "description": "this is an updated segment",
    "status": 1
}

new_award = {
    "uuid": test_uuids.award_uuid,
    "name": "pytest Award",
    "description": "Just a pytest award",
    "channel": 2,
    "award_type": 2,
    "value": 5000
}

update_award = {
    "name": "pytest Award UPDATE",
    "description": "Just a pytest award UPDATE",
    "hero_image": "new_hero_image.jpeg",
    "channel": 4,
    "award_type": 1,
    "value": 10000
}

new_client_award = {
    "award_uuid": test_uuids.award_uuid,
    "name": "pytest Client Award",
    "description": "Just a pytest client award",
    "hero_image": None
}

update_client_award = {
    "name": "pytest Client Award UPDATE",
    "description": "Just a pytest client award UPDATE",
    "hero_image": None
}

new_program_award = {
    "name": "pytest Program Award",
    "description": "Just a pytest program award",
    "hero_image": None
}

update_program_award = {
    "name": "pytest Program Award UPDATE",
    "description": "Just a pytest program award UPDATE",
    "hero_image": None
}

new_segment_award = {
    "client_award_9char": None,
    "name": "pytest Segment Award Test",
    "description": "Just a pytest segment award",
    "hero_image": None
}

update_segment_award = {
    "name": "pytest Segment Award Test UPDATE",
    "description": "Just a pytest segment award UPDATE",
    "hero_image": None
}

new_static_budget = {
    "name": "static Budget pytest",
    "value": 1000,
    "parent_9char": None,
    "active": "True",
    "budget_type": 0
}

update_static_budget = {
    "name": "UPDATED static Budget pytest",
    "value": 500,
    "parent_9char": None,
    "budget_type": 0,
    "active": "True"
}

# check if you need this, or if you can just use "new_static_budget"
new_parent_static_budget = {
    "name": "parent static Budget pytest",
    "value": 500,
    "parent_9char": None,
    "active": "True",
    "budget_type": 0
}

# check if you need this, or if you can just use "new_static_budget"
new_sub_static_budget = {
    "name": "sub static Budget pytest",
    "value": 1000,
    "parent_9char": None,
    "active": "True",
    "budget_type": 0
}

new_parent_budget_no_cap = {
    "name": "Parent Budget pytest with no cap",
    "value": 0,
    "parent_9char": None,
    "active": "True",
    "budget_type": 1
}

new_parent_budget_cap = {
    "name": "Parent Budget pytest with cap",
    "value": 2000,
    "parent_9char": None,
    "active": "True",
    "budget_type": 2
}

new_sub_budget_no_cap = {
    "name": "sub Budget pytest with no cap",
    "value": 0,
    "parent_9char": None,
    "active": "True",
    "budget_type": 1
}

new_sub_budget_cap = {
    "name": "sub Budget pytest with cap",
    "value": 2000,
    "parent_9char": None,
    "active": "True",
    "budget_type": 2
}

new_program_rule = {
    "rule_type": 1,
    "status": 2,
    "logic": {
        "conditions": [
            {
            "var": "hire_anniversary",
            "operator": "=",
            "value": "today"
            }
        ],
        "details": {
            "award_type": "1",
            "client_award": "client_award_uuid",
            "program_award": "program_award_uuid",
            "message": "message_uuid"
        }
    }
}

update_program_rule = {
    "rule_type": 2,
    "status": 1,
    "logic": {"condition": "UPDATED logic"}
}

new_segment_rule = {
    "rule_type": 1,
    "status": 1,
    "logic": {
        "conditions": [
            {
            "var": "hire_anniversary",
            "operator": "=",
            "value": "today"
            }
        ],
        "details": {
            "award_type": "1",
            "client_award": "client_award_uuid",
            "program_award": "program_award_uuid",
            "segment_award": "segment_award_uuid",
            "message": "message_uuid"
        }
    }
}

update_segment_rule = {
    "rule_type": 2,
    "status": 3,
    "logic": {"condition": "UPDATED logic"}
}

new_segment_design = {
    "channel": 1,
    "status": 1,
    "message_uuid": "message_uuid"
}

update_segment_design = {
    "channel": 2,
    "status": 3,
}

new_message = {
    "name": "Pytest Message Test",
    "body": "a message body - Message Test",
    "channel": 2,
    "message_type": 2,
    "status": 1
}

new_program_message = {
    "name": "Pytest Program Message Test",
    "body": "a message body - Message Test",
    "channel": 2,
    "message_type": 2,
    "status": 1
}

new_segment_message = {
    "name": "Pytest Segment Message Test",
    "body": "a message body - Message Test",
    "channel": 2,
    "message_type": 2,
    "status": 1
}

update_message = {
    "name": "UPDATED Pytest Message Test",
    "message_type": 2,
    "channel": 2,
    "status": 1,
    "body": "UPDATED Body Message Test"
}

new_client_message = {
    "name": "Pytest Message Test",
    "body": "a message body - Message Test",
    "client_uuid": test_uuids.first_client_uuid,
    "channel": 2,
    "message_type": 2,
    "status": 1
}
