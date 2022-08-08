"""Module for swagger document generation"""
from flask_restx import fields

from ..extension import api

login_signup_model = api.model('Signin Signup.tsx Parameters', {
    'username': fields.String,
    'password': fields.String
})

user_model = api.model('User', {
    'id': fields.Integer,
    'username': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String,
    'email_verified': fields.String,
    'password': fields.String,
    'phone': fields.String,
    'role': fields.String
})
