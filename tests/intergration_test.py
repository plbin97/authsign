import time

from werkzeug.test import TestResponse
from src.authsign.databaseModels import User
from src.authsign.utils.jwt import stop_jwt_activity_manager_thread


def getLoginData(expiredInSec=0):
    if expiredInSec == 0:
        return {
            "username": "testing",
            "password": "thisismypassword"
        }
    return {
        "username": "testing",
        "password": "thisismypassword",
        "expiredAfterSec": expiredInSec
    }


def getAuthHeader(token: str):
    return {
        'X-API-Key': token
    }


responseAPITokenFromSignUp = ''
responseAPITokenFromLogin = ''


def test_integrationTestInit(newApp):
    with newApp.app_context():
        User.delete_user(user_name=getLoginData()['username'])


def test_signUp(client):
    response: TestResponse = client.post('/authsign/user', json=getLoginData())
    assert response.mimetype == 'text/plain'
    assert response.status_code == 200
    assert len(response.text) > 3
    global responseAPITokenFromSignUp
    responseAPITokenFromSignUp = response.text
    errResponse: TestResponse = client.post('/authsign/user', json=getLoginData())
    assert errResponse.status_code == 400
    assert errResponse.text == 'Your username has already been used'


def test_logIn(client):
    response: TestResponse = client.post('/authsign/userlogin', json=getLoginData())
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
        assert 'first_name' in responseBody
        assert 'last_name' in responseBody
        assert 'email' in responseBody
        assert 'email_verified' in responseBody
        assert 'password' in responseBody
        assert 'phone' in responseBody
        assert 'role' in responseBody
        assert len(responseBody) == 9

    response: TestResponse = client.get('/authsign/user', headers=getAuthHeader('123'))
    assert response.status_code == 401
    response: TestResponse = client.get('/authsign/user')
    assert response.status_code == 401


def test_editUserInfo(client):
    updateData = {
        'first_name': 'Linbin',
        'last_name': 'Pang'
    }
    errorUpdateData = {
        'username': getLoginData()['username']
    }
    response: TestResponse = client.put('/authsign/user', json=updateData,
                                        headers=getAuthHeader(responseAPITokenFromLogin))
    assert response.status_code == 200

    response: TestResponse = client.get('/authsign/user', headers=getAuthHeader(responseAPITokenFromLogin))
    responseBody = response.json
    assert responseBody['first_name'] == updateData['first_name']
    assert responseBody['last_name'] == updateData['last_name']

    response: TestResponse = client.put('/authsign/user', json=errorUpdateData,
                                        headers=getAuthHeader(responseAPITokenFromLogin))
    assert response.status_code == 400
    assert response.text == 'Your username has already been used'


def test_logout(client):
    response: TestResponse = client.get('/authsign/user', headers=getAuthHeader(responseAPITokenFromLogin))
    assert response.status_code == 200
    response: TestResponse = client.get('/authsign/userlogout', headers=getAuthHeader(responseAPITokenFromLogin))
    assert response.status_code == 200
    response: TestResponse = client.get('/authsign/user', headers=getAuthHeader(responseAPITokenFromLogin))
    assert response.status_code == 401
    response: TestResponse = client.get('/authsign/userlogout')
    assert response.status_code == 400


def test_timeoutTest(client):
    response: TestResponse = client.post('/authsign/userlogin', json=getLoginData(5))
    assert response.status_code == 200
    token5Sec = response.text
    response: TestResponse = client.post('/authsign/userlogin', json=getLoginData(2))
    assert response.status_code == 200
    token2Sec = response.text

    response: TestResponse = client.get('/authsign/user', headers=getAuthHeader(token2Sec))
    assert response.status_code == 200
    response: TestResponse = client.get('/authsign/user', headers=getAuthHeader(token5Sec))
    assert response.status_code == 200

    time.sleep(3)
    response: TestResponse = client.get('/authsign/user', headers=getAuthHeader(token2Sec))
    assert response.status_code == 401
    response: TestResponse = client.get('/authsign/user', headers=getAuthHeader(token5Sec))
    assert response.status_code == 200

    time.sleep(3)
    response: TestResponse = client.get('/authsign/user', headers=getAuthHeader(token5Sec))
    assert response.status_code == 401


def test_integrationTestEnd(app):
    with app.app_context():
        User.delete_user(user_name=getLoginData()['username'])
        stop_jwt_activity_manager_thread()
