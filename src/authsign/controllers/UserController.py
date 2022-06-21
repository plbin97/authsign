from flask_restx import Resource
from flask import request, make_response, Response
import json

from ..databaseModels import User
from .userVerification import userVerification
from ..utils.jwt import createJwtForLogin
from ..extension import api
from .swaggerModels import loginSignupModel, userModel



class UserController(Resource):

    @api.doc(security='apikey')
    @api.response(200, 'Success', userModel)
    @api.response(401, 'Unauthorized')
    @api.produces(['application/json'])
    def get(self):
        """
        For getting the user(self) information
        Get the self user's model, but the password field would be empty
        """
        try:
            user = userVerification()
        except PermissionError as err:
            return err.args[0]

        userDict: dict = user.toDict()
        response: Response = make_response(json.dumps(userDict), 200)
        response.mimetype = 'application/json'
        return response

    @api.expect(loginSignupModel)
    @api.response(200, 'Api Token')
    @api.response(400, 'Value Error')
    @api.produces(['text/plain'])
    def post(self):
        """
        For sign up
        Passing a new username and password
        A new token would be generated if successfully sign up.
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
    @api.expect(userModel)
    @api.produces(['text/plain'])
    def put(self):
        """
        For update user's profile
        Passing the fields you are going to update with values
        However, update of ID, emailVerified, and role would not work.
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
