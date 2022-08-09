"""
Singleton application for testing
"""
from app import app, create_app

APP_INST = app


def get_app():
    """
    Get app
    :return:
    """
    return APP_INST


def refresh_app():
    """
    create a new app that cover the original one
    :return:
    """
    global APP_INST
    APP_INST = create_app()
    APP_INST.config.update({
        "TESTING": True,
    })
    APP_INST.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    APP_INST.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = None
    return APP_INST


refresh_app()
