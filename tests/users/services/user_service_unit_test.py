# import io
# import csv
# import pytest
# from fastapi.testclient import TestClient
# from fastapi import FastAPI
# from app.routers.v1.users.user_router import router as user_router
# from app.actions.users import user_actions
# from .dependencies import override_check_existing

# app = FastAPI()
# app.include_router(user_router)
# client = TestClient(app)

# TODO: Work in progress
# def test_create_service(override_check_existing):
#     # Test case 1: UserService already exists
#     response = client.post(
#         f"/services/{user_uuid}",
#         json={
#             "service_uuid": service_uuid,
#             "service_user_id": service_user_id,
#         },
#     )
#     assert response.status_code == 200
#     assert response.json() == {
#         "user_uuid": user_uuid,
#         "service_uuid": service_uuid,
#         "service_user_id": service_user_id,
#         "service_user_screenname": "Test User",
#         "service_user_name": "Test User",
#         "service_access_token": "test_access_token",
#         "service_access_secret": "test_access_secret",
#         "service_refresh_token": "test_refresh_token",
#         "time_created": 0,
#         "time_updated": 0,
#         "uuid": "test_uuid",
#         "status": "existing",
#     }

#     # Test case 2: UserService does not exist and is created
#     new_service_user_id = "new_test@example.com"
#     response = client.post(
#         f"/services/{user_uuid}",
#         json={
#             "service_uuid": service_uuid,
#             "service_user_id": new_service_user_id,
#         },
#     )
#     # You should change the following assertions to match your actual implementation
#     assert response.status_code == 200
#     assert "uuid" in response.json()
#     assert response.json()["user_uuid"] == user_uuid
#     assert response.json()["service_uuid"] == service_uuid
#     assert response.json()["service_user_id"] == new_service_user_id

# def test_create_users_from_csv(mocker):
# 	# Mock the create_users_from_csv function
# 	test_users = [
# 		{
# 			"legal_first_name": "Gwendolyn", "legal_last_name": "Choi", "primary_work_email": "gwendolyn.choi@testclient.com", "hire_date": "1/1/15", "continuous_service_date": "1/1/15", "employee_id": 1139, "manager_id": 200405, "cost_center_id": 21121, "worker_type": "Employee", "department": "NAMER Sales-East-NY", "manager": "Marion Hargett", "location": "New York", "business_title": "GM, Business Development East", "department_leader": 200405
# 		},
# 		{
# 			"Legal First Name": "Khari", "Legal Last Name": "Vaughn", "Primary Work Email": "khari.vaughn@testclient.com", "Hire Date": "1/1/19", "Continuous Service Date": "1/1/19", "Employee ID": 102246, "Manager ID": 200405, "Cost Center - ID": 43020, "Worker Type": "Employee", "Department": "Engineering", "Manager": "Kenny Ayers", "Location": "New York", "Business Title": "Software Engineer II", "Department Leader": 200405
# 		}
# 	]
# 	mocker.patch.object(users_actions, 'create_users_from_csv', return_value=test_users)

# 	# Create a mock CSV file for testing
# 	file_data = io.StringIO()
# 	writer = csv.DictWriter(file_data, fieldnames=["name", "email"])
# 	writer.writeheader()
# 	for user in test_users:
# 		writer.writerow(user)
# 	file_data.seek(0)

# 	# Simulate file upload
# 	response = client.post("/users/upload_csv", files={"file": ("test_users.csv", file_data.getvalue(), "text/csv")})
# 	assert response.status_code == 201
# 	assert response.json() == {"message": f"Created {len(test_users)} users"}
