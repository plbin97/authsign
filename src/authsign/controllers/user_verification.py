"""Helper module for user verification"""
from flask import request, Response, make_response

from ..database_models import User
from ..utils.jwt import verify_jwt


def user_verification() -> User:
    """
    This is a helper function for controller;
    it read token from request header for verifying user's identity
    :return:
    a user model if request is valid.
    If the request is invalid, a PermissionError would be raised.
        The first argument would be the response for controller to return
    """
    response: Response = make_response()
    response.status_code = 401
    response.data = 'Signin expired'
    if 'X-Api-Key' not in request.headers:
        raise PermissionError(response)
    user_token: str = request.headers['X-Api-Key']
    try:
        user_id, = verify_jwt(user_token)# pylint: disable=unbalanced-tuple-unpacking
    except LookupError as exc:
        raise PermissionError(response) from exc
    if user_id is None:
        raise PermissionError(response)
    user: User = User.query.filter_by(id=user_id).first()
    if user is None:
        raise PermissionError(response)

    return user
