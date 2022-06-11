import time

from .jwtActivityManager import isJwtActive, activateJwt, stopThread

def test():
    jwtHash = 123
    activateJwt(jwtHash, 1)
    assert isJwtActive(jwtHash) is True
    time.sleep(3)
    assert isJwtActive(jwtHash) is False
    stopThread()
