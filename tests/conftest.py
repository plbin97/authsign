import pytest
from .appForTesting import getApp, refreshApp


@pytest.fixture()
def app():
    return getApp()


@pytest.fixture()
def newApp():
    return refreshApp()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
