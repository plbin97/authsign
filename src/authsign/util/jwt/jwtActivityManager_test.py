import time
import threading

from .jwtActivityManager import isJwtActive, activateJwt, stopJwtActivityManagerThread, disableJwt, \
    startJwtActivityManagerThread


def test():
    startJwtActivityManagerThread()
    jwtHash = 12345
    activateJwt(jwtHash, 1)
    assert isJwtActive(jwtHash) is True
    time.sleep(3)
    assert isJwtActive(jwtHash) is False
    activateJwt(jwtHash, 100)
    assert isJwtActive(jwtHash) is True
    disableJwt(jwtHash)
    assert isJwtActive(jwtHash) is False
    stopJwtActivityManagerThread()
