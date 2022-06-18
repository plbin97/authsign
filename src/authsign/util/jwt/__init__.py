from .JwtCodec import JwtCodec
from .jwtActivityManager import activateJwt, isJwtActive, disableJwt, stopJwtActivityManagerThread, \
    startJwtActivityManagerThread, activeJwtHash


def createJwtForLogin(userID: int, role: int = 0) -> str:
    """
    Create a Jwt for login.
    This jwt would be active for 2 hours
    :param userID:
    :param role:
    :return: jwt
    """
    jwtCodec: JwtCodec = JwtCodec.newJwt(userID=userID, role=role)
    activateJwt(jwtCodec.getJwtHash())
    return jwtCodec.getJwtStr()


def verifyJwt(jwtStr: str) -> (int, int) or (None, None):
    """
    Verify a Jwt, check if the JWT is valid and unexpired
    :param jwtStr:
    :return:
    For invalid or expired JWT, return (None, None)
    For valid JWT, return (userID, role)
    """
    jwtCodec: JwtCodec = JwtCodec.fromJwtStr(jwtStr)
    if jwtCodec is None:
        return None, None
    if jwtCodec.isExpired():
        return None, None

    if not isJwtActive(hash(jwtStr)):
        return None, None

    return jwtCodec.userID, jwtCodec.role


def disableJwtForLogout(jwtStr: str):
    """
    Disable a JWT for logout
    :param jwtStr:
    :return:
    """
    disableJwt(hash(jwtStr))
