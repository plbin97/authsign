import time
import threading

from src.authsign.utils.jwt.jwt_activity_manager import is_jwt_active, activate_jwt, stop_jwt_activity_manager_thread, disable_jwt, \
    start_jwt_activity_manager_thread


def test():
    start_jwt_activity_manager_thread()
    jwtHash = 12345
    activate_jwt(jwtHash, 1)
    assert is_jwt_active(jwtHash) is True
    time.sleep(3)
    assert is_jwt_active(jwtHash) is False
    activate_jwt(jwtHash, 100)
    assert is_jwt_active(jwtHash) is True
    disable_jwt(jwtHash)
    assert is_jwt_active(jwtHash) is False
    stop_jwt_activity_manager_thread()
