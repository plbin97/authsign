"""
Unit test
"""
import time

from src.authsign.utils.jwt.jwt_activity_manager \
    import is_jwt_active, \
    activate_jwt, \
    stop_jwt_activity_manager_thread, \
    disable_jwt, \
    start_jwt_activity_manager_thread


def test():
    """
    test
    :return:
    """
    start_jwt_activity_manager_thread()
    jwt_hash = 12345
    activate_jwt(jwt_hash, 1)
    assert is_jwt_active(jwt_hash) is True
    time.sleep(3)
    assert is_jwt_active(jwt_hash) is False
    activate_jwt(jwt_hash, 100)
    assert is_jwt_active(jwt_hash) is True
    disable_jwt(jwt_hash)
    assert is_jwt_active(jwt_hash) is False
    stop_jwt_activity_manager_thread()
