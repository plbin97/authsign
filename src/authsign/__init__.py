"""Flask start up file"""
from flask import Blueprint, send_from_directory, Flask
from flask_cors import CORS
from .utils.jwt import start_jwt_activity_manager_thread
from .extension import db, migrate, api

from .controllers import UserLoginController, UserController, UserLogoutController

authsign: Blueprint = Blueprint(
    'authsign', __name__,
    static_folder='client/build',
    static_url_path='/authsign'
)
cors = CORS(authsign)


@authsign.record
def on_register(setup_state):
    """
    Hooker on registered
    :param setup_state:
    :return:
    """
    app: Flask = setup_state.app
    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)
    start_jwt_activity_manager_thread()

    authorizations = {
        'apikey': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'X-Api-Key'
        }
    }
    api.authorizations = authorizations
    api.title = 'Authsign API'
    api.description = 'A user management blueprint'
    api.version = '1.0'


@authsign.route('/authsign')
def client():
    """
    Client route
    :return:
    """
    return send_from_directory(authsign.static_folder, 'index.html')


@api.route('/authsign/user')
class UC(UserController):
    """
    User controller route
    """


@api.route('/authsign/userlogin')
class ULIC(UserLoginController):
    """
    User login route
    """


@api.route('/authsign/userlogout')
class ULOC(UserLogoutController):
    """
    user logout route
    """
