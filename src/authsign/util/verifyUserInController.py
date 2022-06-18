from flask import request

from src.authsign.databaseModels import User
from src.authsign.util.jwt import verifyJwt


def verifyUserInController() -> tuple or User:
    """
    This is a helper function for controller;
    it read token from request header for verifying user's identity
    :return:
    a tuple if request is invalid, the tuple represent the error that could directly return in controller
    a user model if request is valid.
    """

    if 'X-Api-Key' not in request.headers:
        return 'No token found', 400
    userToken: str = request.headers['X-Api-Key']
    userID, role = verifyJwt(userToken)
    if userID is None:
        return 'No token found', 400
    user: User = User.query.filter_by(id=userID).first()
    if user is None:
        return 'User not found', 400

    return user
