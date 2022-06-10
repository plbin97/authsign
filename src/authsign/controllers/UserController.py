from flask_restx import Resource, reqparse
from flask import request
import hashlib

from ..databaseModels import User
from ..extension import db
from ..util.hashPassword import hashPassword

parser = reqparse.RequestParser


class UserController(Resource):

    def get(self):
        return {'hello': 'world'}

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
