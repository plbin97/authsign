"""
A helper for getting username and password from request data
"""
from flask import request


def get_username_password_helper() -> (str, str):
    """
    Get username and password from request
    :return:
    """
    req_data: dict = request.json

    if ('username' not in req_data) or ('password' not in req_data):
        raise KeyError

    username: str = req_data['username']
    password: str = req_data['password']
    return username, password
