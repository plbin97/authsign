"""
Unit test for hash password
"""
from src.authsign.utils.hash_password import hash_password

def test():
    """
    test
    :return:
    """
    hashed: str = hash_password('123')
    assert len(hashed) == 32
