from flask import request, Response, make_response

from src.authsign.databaseModels import User
from src.authsign.utils.jwt import verifyJwt


def userVerification() -> Response or User:
    """
    This is a helper function for controller;
    it read token from request header for verifying user's identity
    :return:
    a response if request is invalid, you just need to return this response in controller.
    a user model if request is valid.
    """

    response: Response = make_response()
    response.status_code = 400
    response.mimetype = 'text/plain'

    if 'X-Api-Key' not in request.headers:
        response.response = 'No token found'
        return response
    userToken: str = request.headers['X-Api-Key']
    userID, role = verifyJwt(userToken)
    if userID is None:
        response.response = 'No token found'
        return response
    user: User = User.query.filter_by(id=userID).first()
    if user is None:
        response.response = 'User not found'
        return response

    return user
