from flask_restx import Resource
from flask import request, make_response, Response

from ..databaseModels import User
from ..utils.jwt import createJwtForLogin


class UserLoginController(Resource):
    def post(self):
        """
        For user login
        Handle the username and password, then return the api token.
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
            user: User = User.getUserByLogin(userName=username, password=password)
        except ValueError as err:
            response.data = err.args[0]
            return response

        response.status_code = 200
        if 'expiredAfterSec' in reqData:
            expiredAfterSec = reqData['expiredAfterSec']
            if isinstance(expiredAfterSec, int):
                response.data = createJwtForLogin(user.id, user.role, expiredAfterSec)
                return response

        response.data = createJwtForLogin(user.id, user.role)
        return response
