"""
Response maker
"""
from flask import Response, make_response


def error_response_factory():
    """
    Create response
    :return:
    """
    response: Response = make_response()
    response.status_code = 400
    response.mimetype = 'text/plain'
    return response
