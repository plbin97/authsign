import random
import string
from datetime import datetime, timedelta
import jwt

jwtSecret = ''.join(random.choices(string.ascii_letters, k=8))


def jwtEncode(userID: int, role: int, hoursOfExpire: int) -> str:
    """
    Produce JWT string by userID and role
    :param userID:
    :param role:
    :param hoursOfExpire:
    :return:
    """
    now = datetime.utcnow()
    expireDatetime = now + timedelta(hours=hoursOfExpire)

    jwtPayload: dict = {
        'utcTimeOfIssue': now.strftime('%c'),
        'utcTimeOfExpire': expireDatetime.strftime('%c'),
        'userID': userID,
        'role': role
    }
    return jwt.encode(jwtPayload, jwtSecret, algorithm='HS256')


def jwtDecode(encodedStr: str, now: datetime = datetime.utcnow()) -> (int, int):
    """
    Decode JWT and get user id and role
    :param encodedStr:
    :param now:
    :return: (userID, role)

    If token is invalid, return (None, None)
    If token is expired, return (None, None)
    """
    try:
        jwtPayload: dict = jwt.decode(encodedStr, jwtSecret, algorithms='HS256')
    except:
        return None, None

    utcTimeOfExpire: datetime = datetime.strptime(jwtPayload['utcTimeOfExpire'], '%c')
    if now > utcTimeOfExpire:
        return None, None
    return jwtPayload['userID'], jwtPayload['role']
