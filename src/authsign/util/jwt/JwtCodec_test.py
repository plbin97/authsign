from .JwtCodec import JwtCodec
from datetime import date, datetime, timedelta

def test_ifWorking():
    userID = 123
    jwtCodec1 = JwtCodec.newJwt(userID=userID)
    jwt = jwtCodec1.encodeToJwtStr()
    assert len(jwt) > 1

    jwtCodec2 = JwtCodec.fromJwtStr(jwt)

    assert jwtCodec1.jwtID == jwtCodec2.jwtID
    assert abs((jwtCodec1.utcTimeOfIssue - jwtCodec2.utcTimeOfIssue).total_seconds()) < 60
    assert abs((jwtCodec1.utcTimeOfExpire - jwtCodec2.utcTimeOfExpire).total_seconds()) < 60
    assert jwtCodec1.role == jwtCodec2.role
    assert jwtCodec1.userID == jwtCodec2.userID
    assert jwtCodec1.isExpired() is False

def test_ifExpired():
    userID = 123
    fakeExpireTime = datetime.utcnow() - timedelta(hours=3)
    jwtCodec = JwtCodec.newJwt(userID=userID, utcTimeOfExpire=fakeExpireTime)
    assert jwtCodec.isExpired() is True
