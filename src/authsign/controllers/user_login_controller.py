"""User login model"""
from flask_restx import Resource
from flask import request, Response

from .error_response_factory import error_response_factory
from .get_username_password_helper import get_username_password_helper
from ..database_models import User
from ..utils.jwt import create_jwt_for_login
from ..extension import api
from .swagger_models import login_signup_model


class UserLoginController(Resource):
    """
    Controller for user login
    """
    @api.expect(login_signup_model)
    @api.response(200, 'Api Token')
    @api.response(400, 'Username or password wrong')
    @api.produces(['text/plain'])
    def post(self):
        """
        For user signin
        Passing the username and password, then response the api token.
        """
        response: Response = error_response_factory()

        try:
            username, password = get_username_password_helper()
            user: User = User.get_user_by_login(user_name=username, password=password)
        except KeyError:
            response.data = 'Lack of parameters'
            return response
        except ValueError as err:
            response.data = err.args[0]
            return response

        req_data: dict = request.json
        response.status_code = 200
        if 'expiredAfterSec' in req_data:
            expired_after_sec = req_data['expiredAfterSec']
            if isinstance(expired_after_sec, int):
                response.data = create_jwt_for_login(user.id, user.role, expired_after_sec)
                return response

        response.data = create_jwt_for_login(user.id, user.role)
        return response
