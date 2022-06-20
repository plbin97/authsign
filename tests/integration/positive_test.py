from werkzeug.test import TestResponse
from src.authsign.databaseModels import User

loginJsonData: dict = {
    "username": "testing",
    "password": "thisismypassword"
}

authHeaders: dict = {
    'X-API-Key': None
}

def test_integrationNormalTestInit(newApp):
    with newApp.app_context():
        User.deleteUser(userName=loginJsonData['username'])


def test_signUp(client):
    response: TestResponse = client.post('/authsign/user', json=loginJsonData)
    assert response.mimetype == 'text/plain'
    assert response.status_code == 200


def test_logIn(client):
    response: TestResponse = client.post('/authsign/userlogin', json=loginJsonData)
    assert response.status_code == 200
    assert response.mimetype == 'text/plain'
    responseAPIToken = response.text
    assert len(responseAPIToken) > 3
    authHeaders['X-API-Key'] = responseAPIToken

def test_getUserInfo(client):
    response: TestResponse = client.get('/authsign/user', headers=authHeaders)
    assert response.status_code == 200
    assert response.mimetype == 'application/json'
    responseBody: dict = response.json
    assert 'id' in responseBody
    assert 'username' in responseBody
    assert 'firstName' in responseBody
    assert 'lastName' in responseBody
    assert 'email' in responseBody
    assert 'emailVerified' in responseBody
    assert 'password' in responseBody
    assert 'phone' in responseBody
    assert 'role' in responseBody
    assert len(responseBody) == 9

