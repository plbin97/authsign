"""
Unit test
"""
from src.authsign.utils.jwt.jwt_codec import JwtCodec
from datetime import datetime, timedelta


def test_if_working():
    """
    General testing
    :return:
    """
    user_id = 123
    jwt_codec1 = JwtCodec.new_jwt(user_id=user_id)
    jwt = jwt_codec1.get_jwt_str()
    assert len(jwt) > 1
    assert len(jwt_codec1.jwt_temp) > 1
    assert jwt_codec1.get_jwt_hash() != 0

    jwt_codec2 = JwtCodec.from_jwt_str(jwt)

    assert abs((jwt_codec1.utc_time_of_issue - jwt_codec2.utc_time_of_issue).total_seconds()) < 60
    assert abs((jwt_codec1.utc_time_of_expire - jwt_codec2.utc_time_of_expire).total_seconds()) < 60
    assert jwt_codec1.role == jwt_codec2.role
    assert jwt_codec1.user_id == jwt_codec2.user_id
    assert jwt_codec1.is_expired() is False

def test_duplicate_jwt():
    """
    Test if JWT is duplicated
    :return:
    """
    user_id = 123
    jwt_codec1 = JwtCodec.new_jwt(user_id=user_id)
    jwt_codec2 = JwtCodec.new_jwt(user_id=user_id)
    assert jwt_codec1.get_jwt_str() != jwt_codec2.get_jwt_str()

def test_if_expired():
    """
    Test if JWT is expired
    :return:
    """
    user_id = 123
    fake_expire_time = datetime.utcnow() - timedelta(hours=3)
    jwt_codec = JwtCodec.new_jwt(user_id=user_id, utc_time_of_expire=fake_expire_time)
    assert jwt_codec.is_expired() is True


def test_if_jwt_invalid():
    """
    Test if JWT is invalid
    :return:
    """
    fake_jwt_str = '12345'
    assert JwtCodec.from_jwt_str(fake_jwt_str) is None
