from flask_restx import Resource
from flask import request
import json

from ..databaseModels import User
from ..extension import db
from ..util.hashPassword import hashPassword
from ..util import verifyUserInController

class UserController(Resource):

    def get(self):
        """
        For getting the user(self) information
        :return:
        """
        verifyResult = verifyUserInController()
        if isinstance(verifyResult, tuple):
            return verifyResult
        user: User = verifyResult
        userDict: dict = user.toDict()
        return json.dumps(userDict), 200

    def post(self):
        """
        For sign up
        Handle the json body with two parameters: username and password
        for more detail: https://plbin97.github.io/authsign/#operations-user-post_user
        :return:
        """
        reqData: dict = request.json

        if ('username' not in reqData) or ('password' not in reqData):
            return 'Lack of parameters', 400

        username: str = reqData['username']
        password: str = reqData['password']

        if len(username) > 32:
            return 'Username is too long', 400
        if len(password) > 32:
            return 'Password is too long', 400
        if User.query.filter_by(username=username).first() is not None:
            return 'Your username has already been used', 400

        passwordHash: str = hashPassword(password)

        newUser = User(username=username, password=passwordHash, emailVerified=False, role=1)
        db.session.add(newUser)
        db.session.commit()
        return 'Done', 200

    def put(self):
        verifyResult = verifyUserInController()
        if isinstance(verifyResult, tuple):
            return verifyResult
        user: User = verifyResult
        reqData: dict = request.json
        user.userUpdateInfo(reqData)
        return '', 200
