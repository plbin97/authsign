from flask import Flask, redirect
from src.authsign.app import authsign
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from src.authsign.extension import db, migrate

app = Flask(__name__, static_folder=None)
app.register_blueprint(authsign)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate.init_app(app, db)
from src.authsign.databaseModels import User


@app.route('/')
def index():
    return redirect('/authsign')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8088)
