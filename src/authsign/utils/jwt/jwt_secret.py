"""
Module for storing JWT secret
"""
import random
import string

JWT_SECRET = ''.join(random.choices(string.ascii_letters, k=8))
