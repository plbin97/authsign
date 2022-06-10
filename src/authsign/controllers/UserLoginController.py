from flask_restx import Resource
from flask import request, jsonify
import jwt

from ..databaseModels import User
from ..util.hashPassword import hashPassword


class UserLoginController(Resource):
    def post(self):
        reqData: dict = request.json
        if ('username' not in reqData) or ('password' not in reqData):
            return 'Lack of parameters', 400

        username: str = reqData['username']
        password: str = reqData['password']

        if len(username) > 32:
            return 'Username is too long', 400
        if len(password) > 32:
            return 'Password is too long', 400

        hashedPassword: str = hashPassword(password)
        user: User = User.query.filter_by(username=username, password=hashedPassword).first()

        if user is None:
            return 'Your username has already been used', 400


        return