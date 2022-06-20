from flask import Flask
from src.authsign import authsign
from src.authsign.extension import db, migrate

def createApp():
    app = Flask(__name__, static_folder=None)
    app.register_blueprint(authsign)
    db.init_app(app)
    migrate.init_app(app, db)
    return app