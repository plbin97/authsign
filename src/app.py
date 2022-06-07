from flask import Blueprint, send_from_directory
from flask_cors import CORS, cross_origin

auth_sign = Blueprint('authsign', __name__, static_folder='client/build', static_url_path='/authsign')
cors = CORS(auth_sign)


@auth_sign.route('/authsign')
def client():
    return send_from_directory(auth_sign.static_folder, 'index.html')


