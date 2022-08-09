"""
Interaction testing
"""
import time

from werkzeug.test import TestResponse
from src.authsign.database_models import User
from src.authsign.utils.jwt import stop_jwt_activity_manager_thread


def get_login_data(expired_in_sec=0):
    """
    Login data mock
    :param expired_in_sec:
    :return:
    """
    if expired_in_sec == 0:
        return {
            "username": "testing",
            "password": "thisismypassword"
        }
    return {
        "username": "testing",
        "password": "thisismypassword",
        "expiredAfterSec": expired_in_sec
    }


def get_auth_header(token: str):
    """
    Get header
    :param token:
    :return:
    """
    return {
        'X-API-Key': token
    }


RESPONSE_API_TOKEN_FROM_SIGN_UP = ''
RESPONSE_API_TOKEN_FROM_LOGIN = ''


def test_integration_test_init(new_app):
    """
    Initializing
    :param new_app:
    :return:
    """
    with new_app.app_context():
        User.delete_user(user_name=get_login_data()['username'])


def test_sign_up(client):
    """
    Sign up test
    :param client:
    :return:
    """
    response: TestResponse = client.post('/authsign/user', json=get_login_data())
    assert response.mimetype == 'text/plain'
    assert response.status_code == 200
    assert len(response.text) > 3
    global RESPONSE_API_TOKEN_FROM_SIGN_UP
    RESPONSE_API_TOKEN_FROM_SIGN_UP = response.text
    err_response: TestResponse = client.post('/authsign/user', json=get_login_data())
    assert err_response.status_code == 400
    assert err_response.text == 'Your username has already been used'


def test_log_in(client):
    """
    Login test
    :param client:
    :return:
    """
    response: TestResponse = client.post('/authsign/userlogin', json=get_login_data())
    assert response.status_code == 200
    assert response.mimetype == 'text/plain'
    assert len(response.text) > 3
    global RESPONSE_API_TOKEN_FROM_LOGIN
    RESPONSE_API_TOKEN_FROM_LOGIN = response.text
    wrong_login_json_data: dict = {
        "username": "testing123",
        "password": "thisismypassword"
    }
    error_response: TestResponse = client.post('/authsign/userlogin', json=wrong_login_json_data)
    assert error_response.status_code == 400
    assert error_response.text == 'Username or password incorrect'


def test_get_user_info(client):
    """
    Get user info test
    :param client:
    :return:
    """
    for token in [RESPONSE_API_TOKEN_FROM_LOGIN, RESPONSE_API_TOKEN_FROM_SIGN_UP]:
        response: TestResponse = client.get('/authsign/user', headers=get_auth_header(token))
        assert response.status_code == 200
        assert response.mimetype == 'application/json'
        response_body: dict = response.json
        assert 'id' in response_body
        assert 'username' in response_body
        assert 'first_name' in response_body
        assert 'last_name' in response_body
        assert 'email' in response_body
        assert 'email_verified' in response_body
        assert 'password' in response_body
        assert 'phone' in response_body
        assert 'role' in response_body
        assert len(response_body) == 9

    response: TestResponse = client.get('/authsign/user', headers=get_auth_header('123'))
    assert response.status_code == 401
    response: TestResponse = client.get('/authsign/user')
    assert response.status_code == 401


def test_edit_user_info(client):
    """
    Edit user info test
    :param client:
    :return:
    """
    update_data = {
        'first_name': 'Linbin',
        'last_name': 'Pang'
    }
    error_update_data = {
        'username': get_login_data()['username']
    }
    response: TestResponse = client.put('/authsign/user', json=update_data,
                                        headers=get_auth_header(RESPONSE_API_TOKEN_FROM_LOGIN))
    assert response.status_code == 200

    response: TestResponse = client.get('/authsign/user', headers=get_auth_header(RESPONSE_API_TOKEN_FROM_LOGIN))
    response_body = response.json
    assert response_body['first_name'] == update_data['first_name']
    assert response_body['last_name'] == update_data['last_name']

    response: TestResponse = client.put('/authsign/user', json=error_update_data,
                                        headers=get_auth_header(RESPONSE_API_TOKEN_FROM_LOGIN))
    assert response.status_code == 400
    assert response.text == 'Your username has already been used'


def test_logout(client):
    """
    Logout test
    :param client:
    :return:
    """
    response: TestResponse = client.get('/authsign/user', headers=get_auth_header(RESPONSE_API_TOKEN_FROM_LOGIN))
    assert response.status_code == 200
    response: TestResponse = client.get('/authsign/userlogout', headers=get_auth_header(RESPONSE_API_TOKEN_FROM_LOGIN))
    assert response.status_code == 200
    response: TestResponse = client.get('/authsign/user', headers=get_auth_header(RESPONSE_API_TOKEN_FROM_LOGIN))
    assert response.status_code == 401
    response: TestResponse = client.get('/authsign/userlogout')
    assert response.status_code == 400


def test_timeout_test(client):
    """
    Timeout testing
    :param client:
    :return:
    """
    response: TestResponse = client.post('/authsign/userlogin', json=get_login_data(5))
    assert response.status_code == 200
    token5_sec = response.text
    response: TestResponse = client.post('/authsign/userlogin', json=get_login_data(2))
    assert response.status_code == 200
    token2_sec = response.text

    response: TestResponse = client.get('/authsign/user', headers=get_auth_header(token2_sec))
    assert response.status_code == 200
    response: TestResponse = client.get('/authsign/user', headers=get_auth_header(token5_sec))
    assert response.status_code == 200

    time.sleep(3)
    response: TestResponse = client.get('/authsign/user', headers=get_auth_header(token2_sec))
    assert response.status_code == 401
    response: TestResponse = client.get('/authsign/user', headers=get_auth_header(token5_sec))
    assert response.status_code == 200

    time.sleep(3)
    response: TestResponse = client.get('/authsign/user', headers=get_auth_header(token5_sec))
    assert response.status_code == 401


def test_integration_test_end(app):
    """
    Ending test
    :param app:
    :return:
    """
    with app.app_context():
        User.delete_user(user_name=get_login_data()['username'])
        stop_jwt_activity_manager_thread()
