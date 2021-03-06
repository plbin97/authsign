import pytest

from src.authsign.utils.jwt import createJwtForLogin, verifyJwt, disableJwtForLogout, stopJwtActivityManagerThread, \
    startJwtActivityManagerThread


def test():
    startJwtActivityManagerThread()
    testUserID = 123
    jwt = createJwtForLogin(userID=testUserID, role=0)
    assert len(jwt) > 1
    userID, role = verifyJwt(jwt)
    assert userID == testUserID
    assert role == 0
    disableJwtForLogout(jwt)
    with pytest.raises(LookupError):
        verifyJwt(jwt)
    stopJwtActivityManagerThread()
