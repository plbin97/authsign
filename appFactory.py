from flask import Flask
from src.authsign import authsign
from src.authsign.extension import db, migrate
from src.authsign.databaseModels import User


def createApp():
    app = Flask(__name__, static_folder=None)
    app.register_blueprint(authsign)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = None
    db.init_app(app)
    migrate.init_app(app, db)

    return app