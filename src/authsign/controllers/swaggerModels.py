from flask_restx import fields

from ..extension import api

loginSignupModel = api.model('Signin Signup.tsx Parameters', {
    'username': fields.String,
    'password': fields.String
})

userModel = api.model('User', {
    'id': fields.Integer,
    'username': fields.String,
    'firstName': fields.String,
    'lastName': fields.String,
    'email': fields.String,
    'emailVerified': fields.String,
    'password': fields.String,
    'phone': fields.String,
    'role': fields.String
})
