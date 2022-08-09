"""
Make sure that swagger document works
"""
from werkzeug.test import TestResponse
from src.authsign.utils.jwt import stop_jwt_activity_manager_thread

def test_init(new_app):
    """
    Initialize
    :param new_app:
    :return:
    """

def test_get_swagger(client):
    """
    Test on getting swagger
    :param client:
    :return:
    """
    response: TestResponse = client.get('/')
    assert response.status_code == 200
    response: TestResponse = client.get('/swagger.json')
    assert response.status_code == 200


def test_end(app):
    """
    End
    :param app:
    :return:
    """
    with app.app_context():
        stop_jwt_activity_manager_thread()
