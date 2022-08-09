"""
conftest
"""
import pytest
from tests.app_for_testing import get_app, refresh_app


@pytest.fixture()
def app():
    """
    Get app
    :return:
    """
    return get_app()


@pytest.fixture()
def new_app():
    """
    Renew the app
    :return:
    """
    return refresh_app()


def client(app):
    """
    get the client
    :return:
    """
    return app.test_client()


def runner(app):
    """
    get the runner
    :return:
    """
    return app.test_cli_runner()
