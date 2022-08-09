"""
Unit test
"""
from src.authsign.utils.jwt.jwt_secret import JWT_SECRET


def test():
    """
    test
    :return:
    """
    assert len(JWT_SECRET) > 0
