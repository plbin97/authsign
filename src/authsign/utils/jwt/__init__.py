"""Module for JWT management"""
from .jwt_codec import JwtCodec
from .jwt_activity_manager import \
    activate_jwt, \
    is_jwt_active, \
    disable_jwt, \
    stop_jwt_activity_manager_thread, \
    start_jwt_activity_manager_thread, \
    ACTIVE_JWT_HASH


def create_jwt_for_login(
        user_id: int,
        role: int = 0,
        time_before_expired_in_sec: int = 7200
) -> str:
    """
    Create a Jwt for signin.
    This jwt would be active for 2 hours
    Also, you could create a short live jwt by passing arg of timeBeforeExpiredInSec
    :param time_before_expired_in_sec: For testing only
    :param user_id:
    :param role:
    :return: jwt
    """
    jwt_codec: JwtCodec = JwtCodec.new_jwt(user_id=user_id, role=role)
    activate_jwt(jwt_codec.get_jwt_hash(), time_before_expired_in_sec)
    return jwt_codec.get_jwt_str()




def verify_jwt(jwt_str: str) -> (int, int):
    """
    Verify a Jwt, check if the JWT is valid and unexpired
    :param jwt_str:
    :return:
    For invalid or expired JWT, a LookupError would be raised
    For valid JWT, return (user_id, role)
    """
    jwt_codec: JwtCodec = JwtCodec.from_jwt_str(jwt_str)
    if jwt_codec is None:
        raise LookupError
    if jwt_codec.is_expired():
        raise LookupError

    if not is_jwt_active(hash(jwt_str)):
        raise LookupError

    return jwt_codec.user_id, jwt_codec.role


def disable_jwt_for_logout(jwt_str: str):
    """
    Disable a JWT for logout
    :param jwt_str:
    :return:
    """
    disable_jwt(hash(jwt_str))
