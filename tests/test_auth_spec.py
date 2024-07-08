from util.util import process_error
from db.repository.organisation import get_organisation
from core.security import create_access_token



def test_register_with_default_organisation(client, db_session):
	data = {
		"firstName": "Mark",
		"lastName": "Test",
		"email":"testuser@hng.com",
		"password":"testing123",
		"phone": "0913277789"
	}
	response = client.post("/auth/register",json=data)
	assert response.status_code == 201
	assert response.json()["status"] == "success"
	user = response.json()['data']['user']
	assert get_organisation(f"{user['firstName']}'s Organisation", db=db_session).name == f"{user['firstName']}'s Organisation"
	assert response.json()["data"]["user"]["email"] == "testuser@hng.com"
	assert response.json()["data"]["user"]["firstName"] == "Mark"
	assert response.json()["data"]["user"]["lastName"] == "Test"
	assert response.json()["data"]["user"]["phone"] == "0913277789"
	access_token = create_access_token(
			data={"sub": response.json()["data"]["user"]["email"]}
	)
	assert response.json()["data"]["accessToken"] == access_token
 
 
def test_login(client, db_session):
	data = {
		"firstName": "Mark",
		"lastName": "Test",
		"email":"testuser@hng.com",
		"password":"testing123",
		"phone": "0913277789"
	}
	response = client.post("/auth/register",json=data)
	data = {
		
		"email":"testuser@hng.com",
		"password":"testing123",
	}
	response = client.post("/auth/login",json=data)
	assert response.status_code == 200
	assert response.json()["status"] == "success"
	user = response.json()['data']['user']
	assert get_organisation(f"{user['firstName']}'s Organisation", db=db_session).name == f"{user['firstName']}'s Organisation"
	assert response.json()["data"]["user"]["email"] == "testuser@hng.com"
	assert response.json()["data"]["user"]["firstName"] == "Mark"
	assert response.json()["data"]["user"]["lastName"] == "Test"
	assert response.json()["data"]["user"]["phone"] == "0913277789"
	access_token = create_access_token(
			data={"sub": response.json()["data"]["user"]["email"]}
	)
	assert response.json()["data"]["accessToken"] == access_token
 
def test_login(client, db_session):
	data = {
		"firstName": "Mark",
		"lastName": "Test",
		"email":"testuser@hng.com",
		"password":"testing123",
		"phone": "0913277789"
	}
	response = client.post("/auth/register",json=data)
	data = {
		
		"email":"testuse1r@hng.com",
		"password":"testing123",
	}
	response = client.post("/auth/login",json=data)
	assert response.status_code == 401
	assert response.json()["statusCode"] == 401

def test_registration_missing_error_message_email(client):
	data = {
		"firstName": "Mark",
		"lastName": "Test",
		"password":"testing123",
		"phone": "0913277789"
	}
	response = client.post("/auth/register",json=data)
	response_data = process_error(response.json()['detail'])
	assert response.status_code == 422
	assert response_data["errors"][0]["field"] == "email"
	 
def test_registration_missing_error_message_password(client):
	data = {
		"firstName": "Mark",
		"lastName": "Test",
		"email":"testuser@hng.com",  
		"phone": "0913277789"
	}
	response = client.post("/auth/register",json=data)
	response_data = process_error(response.json()['detail'])
	assert response.status_code == 422
	assert response_data["errors"][0]["field"] == "password"
	 
def test_registration_missing_error_message_lastName(client):
	data = {
		"firstName": "Mark",
		"email":"testuser@hng.com",  
		"password":"testing123",
		"phone": "0913277789"
	}
	response = client.post("/auth/register",json=data)
	response_data = process_error(response.json()['detail'])
	assert response.status_code == 422
	assert response_data["errors"][0]["field"] == "lastName"
	 
def test_registration_missing_error_message_firstName(client):
	data = {
		"lastName": "Test",
		"email":"testuser@hng.com",
		"password":"testing123",
		"phone": "0913277789"
	}
	response = client.post("/auth/register",json=data)
	response_data = process_error(response.json()['detail'])
	assert response.status_code == 422
	assert response_data["errors"][0]["field"] == "firstName"
	 
