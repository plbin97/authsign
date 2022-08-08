"""Factory for app"""
from flask import Flask
from src.authsign import authsign
from src.authsign.extension import db, migrate

def create_app():
    """
    Factory for creating the app
    :return:
    """
    app = Flask(__name__, static_folder=None)
    app.register_blueprint(authsign)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = None
    db.init_app(app)
    migrate.init_app(app, db)

    return app
