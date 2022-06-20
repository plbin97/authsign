from flask_restx import Resource
from flask import request, make_response, Response
import json

from ..databaseModels import User
from ..extension import db
from ..utils.hashPassword import hashPassword
from .userVerification import userVerification

class UserController(Resource):

    def get(self):
        """
        For getting the user(self) information
        :return:
        """
        verifyResult: Response or User = userVerification()
        if isinstance(verifyResult, Response):
            return verifyResult
        user: User = verifyResult
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
        if User.query.filter_by(username=username).first() is not None:
            response.response = 'Your username has already been used'
            return response

        passwordHash: str = hashPassword(password)

        newUser = User(username=username, password=passwordHash, emailVerified=False, role=1)
        db.session.add(newUser)
        db.session.commit()
        response.status_code = 200
        response.response = 'Done'
        return response

    def put(self):
        verifyResult = userVerification()
        if isinstance(verifyResult, tuple):
            return verifyResult
        user: User = verifyResult
        reqData: dict = request.json
        user.userUpdateInfo(reqData)
        return '', 200
