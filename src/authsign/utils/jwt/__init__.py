from .JwtCodec import JwtCodec
from .jwtActivityManager import activateJwt, isJwtActive, disableJwt, stopJwtActivityManagerThread, \
    startJwtActivityManagerThread, activeJwtHash


def createJwtForLogin(userID: int, role: int = 0, timeBeforeExpiredInSec: int = 7200) -> str:
    """
    Create a Jwt for login.
    This jwt would be active for 2 hours
    Also, you could create a short live jwt by passing arg of timeBeforeExpiredInSec
    :param timeBeforeExpiredInSec: For testing only
    :param userID:
    :param role:
    :return: jwt
    """
    jwtCodec: JwtCodec = JwtCodec.newJwt(userID=userID, role=role)
    activateJwt(jwtCodec.getJwtHash(), timeBeforeExpiredInSec)
    return jwtCodec.getJwtStr()




def verifyJwt(jwtStr: str) -> (int, int):
    """
    Verify a Jwt, check if the JWT is valid and unexpired
    :param jwtStr:
    :return:
    For invalid or expired JWT, a LookupError would be raised
    For valid JWT, return (userID, role)
    """
    jwtCodec: JwtCodec = JwtCodec.fromJwtStr(jwtStr)
    if jwtCodec is None:
        raise LookupError
    if jwtCodec.isExpired():
        raise LookupError

    if not isJwtActive(hash(jwtStr)):
        raise LookupError

    return jwtCodec.userID, jwtCodec.role


def disableJwtForLogout(jwtStr: str):
    """
    Disable a JWT for logout
    :param jwtStr:
    :return:
    """
    disableJwt(hash(jwtStr))
