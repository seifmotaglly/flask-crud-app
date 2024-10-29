import requests

BASE_URL = "http://localhost:8080"

def test_signup():
    url = f"{BASE_URL}/signup"
    payload = {
        "name": "Test User",
        "email": "testuser",
        "password": "password123"
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 201
    assert response.json()["msg"] == "User registered successfully"
    

def test_login():
    url = f"{BASE_URL}/login"
    payload = {
        "email": "testuser",
        "password": "password123"
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_create_organization():
    # First, log in to get the access token
    login_url = f"{BASE_URL}/login"
    login_payload = {
        "email": "testuser",
        "password": "password123"
    }
    login_response = requests.post(login_url, json=login_payload)
    access_token = login_response.json()["access_token"]

    # Now, create an organization using the access token
    url = f"{BASE_URL}/organization"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    payload = {
        "name": "Test Organization",
        "description": "This is a test organization."
    }
    response = requests.post(url, json=payload, headers=headers)
    assert response.status_code == 200
    assert "organization_id" in response.json()


def test_refresh_token():
    # First, log in to get the refresh token
    login_url = f"{BASE_URL}/login"
    login_payload = {
        "email": "testuser",
        "password": "password123"
    }
    login_response = requests.post(login_url, json=login_payload)
    refresh_token = login_response.json()["refresh_token"]

    # Now, refresh the token
    url = f"{BASE_URL}/refresh-token"
    payload = {
        "refresh_token": refresh_token
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "new_refresh_token" in response.json()


def test_revoke_refresh_token():
    # First, log in to get the refresh token
    login_url = f"{BASE_URL}/login"
    login_payload = {
        "email": "testuser",
        "password": "password123"
    }
    login_response = requests.post(login_url, json=login_payload)
    refresh_token = login_response.json()["refresh_token"]
    access_token = login_response.json()["access_token"]

    # Now, revoke the refresh token
    url = f"{BASE_URL}/revoke-refresh-token"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    payload = {
        "refresh_token": refresh_token
    }
    response = requests.post(url, json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json()["msg"] == "Refresh token successfully revoked"
    
    
def test_get_organizations():
    # First, log in to get the access token
    login_url = f"{BASE_URL}/login"
    login_payload = {
        "email": "testuser",
        "password": "password123"
    }
    login_response = requests.post(login_url, json=login_payload)
    access_token = login_response.json()["access_token"]
    
    # Second, create an organization
    url = f"{BASE_URL}/organization"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    payload = {
        "name": "Test Organization",
        "description": "This is a test organization."
    }
    requests.post(url, json=payload, headers=headers)

    # Now, get the organizations using the access token
    url = f"{BASE_URL}/organization"
    
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    assert len(response.json()) > 0
    
    
def test_get_organization():
    # First, log in to get the access token
    login_url = f"{BASE_URL}/login"
    login_payload = {
        "email": "testuser",
        "password": "password123"
    }
    login_response = requests.post(login_url, json=login_payload)
    access_token = login_response.json()["access_token"]
    
    # Create an organization
    url = f"{BASE_URL}/organization"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    payload = {
        "name": "Test Organization",
        "description": "This is a test organization."
    }
    create_response = requests.post(url, json=payload, headers=headers)
    organization_id = create_response.json()["organization_id"]

    # Now, get the organizations using the access token
    url = f"{BASE_URL}/organization/{organization_id}"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()["_id"] == organization_id
    

def test_delete_organization():
    # First, log in to get the access token
    login_url = f"{BASE_URL}/login"
    login_payload = {
        "email": "testuser",
        "password": "password123"
    }
    login_response = requests.post(login_url, json=login_payload)
    access_token = login_response.json()["access_token"]
    
    # Second, create an organization
    url = f"{BASE_URL}/organization"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    payload = {
        "name": "Test Organization",
        "description": "This is a test organization."
    }
    create_response = requests.post(url, json=payload, headers=headers)
    organization_id = create_response.json()["organization_id"]
    
    # Now, delete the organization using the access token
    url = f"{BASE_URL}/organization/{organization_id}"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.delete(url, headers=headers)
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()["msg"] == "Organization deleted successfully"
    

def test_update_organization():
    # First, log in to get the access token
    login_url = f"{BASE_URL}/login"
    login_payload = {
        "email": "testuser",
        "password": "password123"
    }
    login_response = requests.post(login_url, json=login_payload)
    access_token = login_response.json()["access_token"]
    
    # Second, create an organization
    url = f"{BASE_URL}/organization"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    payload = {
        "name": "Test Organization",
        "description": "This is a test organization."
    }
    create_response = requests.post(url, json=payload, headers=headers)
    organization_id = create_response.json()["organization_id"]
    
    # Now, update the organization using the access token
    url = f"{BASE_URL}/organization/{organization_id}"
    payload = {
        "name": "Updated Test Organization",
        "description": "This is an updated test organization."
    }
    response = requests.put(url, json=payload, headers=headers)
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()["msg"] == "Organization updated successfully"


def test_invite_member():
    # First, log in to get the access token
    login_url = f"{BASE_URL}/login"
    login_payload = {
        "email": "testuser",
        "password": "password123"
    }
    login_response = requests.post(login_url, json=login_payload)
    access_token = login_response.json()["access_token"]
    
    # Second, create an organization
    url = f"{BASE_URL}/organization"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    payload = {
        "name": "Test Organization",
        "description": "This is a test organization."
    }
    create_response = requests.post(url, json=payload, headers=headers)
    organization_id = create_response.json()["organization_id"]
    
    # Third, create a new user to invite
    url = f"{BASE_URL}/signup"
    payload = {
        "name": "New User",
        "email": "newuser",
        "password": "password123"
    }
    requests.post(url, json=payload)
    
    # Now, invite the new user to the organization
    url = f"{BASE_URL}/organization/{organization_id}/invite"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    payload = {
        "email": "newuser"
    }
    response = requests.post(url, json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json()["msg"] == "User invited successfully"
    
    