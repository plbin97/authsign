"""
JWT integration test
"""
import pytest

from src.authsign.utils.jwt \
    import create_jwt_for_login, \
    verify_jwt, \
    disable_jwt_for_logout, \
    stop_jwt_activity_manager_thread, \
    start_jwt_activity_manager_thread


def test():
    """
    test
    :return:
    """
    start_jwt_activity_manager_thread()
    test_user_id = 123
    jwt = create_jwt_for_login(user_id=test_user_id, role=0)
    assert len(jwt) > 1
    user_id, role = verify_jwt(jwt)
    assert user_id == test_user_id
    assert role == 0
    disable_jwt_for_logout(jwt)
    with pytest.raises(LookupError):
        verify_jwt(jwt)
    stop_jwt_activity_manager_thread()
