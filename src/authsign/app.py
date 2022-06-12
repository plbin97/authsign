from flask import Blueprint, send_from_directory
from flask_cors import CORS
from flask_restx import Api
from flask import Flask
from .util.jwt import startJwtActivityManagerThread
from .extension import db, migrate

from .controllers import UserLoginController, UserController, UserLogoutController

authsign: Blueprint = Blueprint('authsign', __name__, static_folder='client/build', static_url_path='/authsign')
cors = CORS(authsign)
api = Api(authsign)


@authsign.record
def onRegister(setupState):
    app: Flask = setupState.app
    db.init_app(app)
    migrate.init_app(app, db)
    startJwtActivityManagerThread()


@authsign.route('/authsign')
def client():
    return send_from_directory(authsign.static_folder, 'index.html')


@api.route('/authsign/user')
class UC(UserController):
    pass


@api.route('/authsign/userlogin')
class ULIC(UserLoginController):
    pass


@api.route('/authsign/userlogout')
class ULOC(UserLogoutController):
    pass
