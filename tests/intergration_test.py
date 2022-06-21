import pytest
from werkzeug.test import TestResponse
from src.authsign.databaseModels import User
from src.authsign.utils.jwt import stopJwtActivityManagerThread

loginJsonData: dict = {
    "username": "testing",
    "password": "thisismypassword"
}


def getAuthHeader(token: str):
    return {
        'X-API-Key': token
    }


responseAPITokenFromSignUp = ''
responseAPITokenFromLogin = ''


def test_integrationTestInit(newApp):
    with newApp.app_context():
        User.deleteUser(userName=loginJsonData['username'])


def test_signUp(client):
    response: TestResponse = client.post('/authsign/user', json=loginJsonData)
    assert response.mimetype == 'text/plain'
    assert response.status_code == 200
    assert len(response.text) > 3
    global responseAPITokenFromSignUp
    responseAPITokenFromSignUp = response.text
    errResponse: TestResponse = client.post('/authsign/user', json=loginJsonData)
    assert errResponse.status_code == 400
    assert errResponse.text == 'Your username has already been used'


def test_logIn(client):
    response: TestResponse = client.post('/authsign/userlogin', json=loginJsonData)
    assert response.status_code == 200
    assert response.mimetype == 'text/plain'
    assert len(response.text) > 3
    global responseAPITokenFromLogin
    responseAPITokenFromLogin = response.text
    wrongLoginJsonData: dict = {
        "username": "testing123",
        "password": "thisismypassword"
    }
    errorResponse: TestResponse = client.post('/authsign/userlogin', json=wrongLoginJsonData)
    assert errorResponse.status_code == 400
    assert errorResponse.text == 'Username or password incorrect'


def test_getUserInfo(client):
    for token in [responseAPITokenFromLogin, responseAPITokenFromSignUp]:
        response: TestResponse = client.get('/authsign/user', headers=getAuthHeader(token))
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

def test_integrationTestEnd(app):
    with app.app_context():
        User.deleteUser(userName=loginJsonData['username'])
        stopJwtActivityManagerThread()
