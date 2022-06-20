from flask_restx import Resource
from flask import request, make_response, Response


from ..databaseModels import User
from ..utils.hashPassword import hashPassword
from ..utils.jwt import createJwtForLogin


class UserLoginController(Resource):
    def post(self):
        """
        Controller for user login
        Handle the username and password, then return the api token.
        :return:
        """
        reqData: dict = request.json

        response: Response = make_response()
        response.status_code = 400
        response.mimetype = 'text/plain'

        if ('username' not in reqData) or ('password' not in reqData):
            response.response = 'Lack of parameters'
            return response

        username: str = reqData['username']
        password: str = reqData['password']

        if len(username) > 32:
            response.response = 'Username is too long'
            return response
        if len(password) > 32:
            response.response = 'Password is too long'
            return response

        hashedPassword: str = hashPassword(password)
        user: User = User.query.filter_by(username=username, password=hashedPassword).first()

        if user is None:
            response.response = 'Username or password incorrect'
            return response

        jwtStr: str = createJwtForLogin(user.id, user.role)
        response.response = jwtStr
        response.status_code = 200
        return response
