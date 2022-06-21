from flask_restx import Resource
from flask import request, make_response, Response
from ..utils.jwt import disableJwtForLogout
from ..extension import api


class UserLogoutController(Resource):

    @api.doc(security='apikey')
    @api.response(200, 'Success')
    @api.response(400, 'Missing header')
    @api.produces(['text/plain'])
    def get(self):
        """
        For log out
        Disable the api token in the header
        """
        response: Response = make_response()
        response.mimetype = 'text/plain'
        if 'X-Api-Key' not in request.headers:
            response.status_code = 400
            response.data = 'Missing Header'
            return response
        response.data = 'Done'
        response.status_code = 200
        disableJwtForLogout(request.headers['X-Api-Key'])
        return response
