from flask_restx import Resource
from flask import request, make_response, Response
import json

from ..databaseModels import User
from .userVerification import userVerification
from ..utils.jwt import createJwtForLogin
from ..extension import api


class UserController(Resource):

    @api.doc(security='apikey')
    def get(self):
        """
        For getting the user(self) information
        :return:
        """
        try:
            user = userVerification()
        except PermissionError as err:
            return err.args[0]

        userDict: dict = user.toDict()
        response: Response = make_response(json.dumps(userDict), 200)
        response.mimetype = 'application/json'
        return response

    def post(self):
        """
        For sign up
        Handle the json body with two parameters: username and password
        for more detail: https://plbin97.github.io/authsign/#operations-user-post_user
        :return:
        """
        reqData: dict = request.json

        response: Response = make_response()
        response.status_code = 400
        response.mimetype = 'text/plain'

        if ('username' not in reqData) or ('password' not in reqData):
            response.data = 'Lack of parameters'
            return response

        username: str = reqData['username']
        password: str = reqData['password']

        try:
            user: User = User.newUser(userName=username, password=password)
        except ValueError as err:
            response.data = err.args[0]
            return response

        jwtStr: str = createJwtForLogin(user.id, user.role)
        response.status_code = 200
        response.data = jwtStr
        return response

    @api.doc(security='apikey')
    def put(self):
        """
        For update user's profile
        :return:
        """
        reqData: dict = request.json
        response: Response = make_response()
        response.mimetype = 'text/plain'
        try:
            user = userVerification()
        except PermissionError as err:
            return err.args[0]
        try:
            user.updateUserByDataMap(reqData)
        except ValueError as err:
            response.status_code = 400
            response.data = err.args[0]
            return response
        response.status_code = 200
        response.data = 'Done'
        return response
