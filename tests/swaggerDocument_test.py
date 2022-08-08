from werkzeug.test import TestResponse
from src.authsign.utils.jwt import stop_jwt_activity_manager_thread

def test_init(newApp):
    pass


def test_signUp(client):
    response: TestResponse = client.get('/')
    assert response.status_code == 200
    response: TestResponse = client.get('/swagger.json')
    assert response.status_code == 200


def test_end(app):
    with app.app_context():
        stop_jwt_activity_manager_thread()
