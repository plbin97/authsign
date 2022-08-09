"""Controller for operation on user"""
import json
from flask_restx import Resource
from flask import request, make_response, Response

from .error_response_factory import error_response_factory
from .get_username_password_helper import get_username_password_helper
from ..database_models import User
from .user_verification import user_verification
from ..utils.jwt import create_jwt_for_login
from ..extension import api
from .swagger_models import login_signup_model, user_model


class UserController(Resource):
    """
    Controller static class
    """

    @api.doc(security='apikey')
    @api.response(200, 'Success', user_model)
    @api.response(401, 'Unauthorized')
    @api.produces(['application/json'])
    def get(self):
        """
        For getting the user(self) information
        Get the self user's model, but the password field would be empty
        """
        try:
            user = user_verification()
        except PermissionError as err:
            return err.args[0]

        user_dict: dict = user.to_dict()
        response: Response = make_response(json.dumps(user_dict), 200)
        response.mimetype = 'application/json'
        return response

    @api.expect(login_signup_model)
    @api.response(200, 'Api Token')
    @api.response(400, 'Value Error')
    @api.produces(['text/plain'])
    def post(self):
        """
        For sign up
        Passing a new username and password
        A new token would be generated if successfully sign up.
        """
        response: Response = error_response_factory()
        try:
            username, password = get_username_password_helper()
            user: User = User.new_user(user_name=username, password=password)
        except ValueError as err:
            response.data = err.args[0]
            return response
        except KeyError:
            response.data = 'Lack of parameters'
            return response

        jwt_str: str = create_jwt_for_login(user.id, user.role)
        response.status_code = 200
        response.data = jwt_str
        return response

    @api.doc(security='apikey')
    @api.expect(user_model)
    @api.produces(['text/plain'])
    def put(self):
        """
        For update user's profile
        Passing the fields you are going to update with values
        However, update of ID, email_verified, and role would not work.
        """
        req_data: dict = request.json
        response: Response = make_response()
        response.mimetype = 'text/plain'
        try:
            user = user_verification()
        except PermissionError as err:
            return err.args[0]
        try:
            user.update_user_by_data_map(req_data)
        except ValueError as err:
            response.status_code = 400
            response.data = err.args[0]
            return response
        response.status_code = 200
        response.data = 'Done'
        return response
