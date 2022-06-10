from flask_restx import Resource


class UserLogoutController(Resource):
    def post(self):
        return {'hello': 'world'}