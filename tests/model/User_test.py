import pytest

from src.authsign.database_models.user import User
from src.authsign.utils.jwt import stop_jwt_activity_manager_thread

testUsername: str = 'panglinbin'
testAnotherUsername: str = 'linbinpang'
testPassword: str = 'thisismypassword'


def test_init(new_app):
    with new_app.app_context():
        User.delete_user(user_name=testUsername)
        User.delete_user(user_name=testAnotherUsername)


def test_newUser(app):
    with app.app_context():
        testUser = User.new_user(user_name=testUsername, password=testPassword)
        assert isinstance(testUser, User)

        with pytest.raises(ValueError, match='.*?been used.*?'):
            User.new_user(user_name=testUsername, password=testPassword)

        with pytest.raises(ValueError, match='.*?too short.*?'):
            User.new_user(user_name='otherUsernameTest', password='123')

        with pytest.raises(ValueError, match='.*?too short.*?'):
            User.new_user(user_name='123', password=testPassword)

        with pytest.raises(ValueError, match='.*?too long.*?'):
            User.new_user(user_name='123' * 100, password=testPassword)

        with pytest.raises(ValueError, match='.*?too long.*?'):
            User.new_user(user_name='otherUsernameTest', password='123' * 100)


def test_loginUser(app):
    with app.app_context():
        testUser = User.get_user_by_login(user_name=testUsername, password=testPassword)
        assert isinstance(testUser, User)
        with pytest.raises(ValueError, match='.*?incorrect.*?'):
            User.get_user_by_login(user_name='123', password=testPassword)
        with pytest.raises(ValueError, match='.*?incorrect.*?'):
            User.get_user_by_login(user_name=testUsername, password='123')
        with pytest.raises(ValueError, match='.*?too long.*?'):
            User.get_user_by_login(user_name=testUsername, password='123' * 100)
        with pytest.raises(ValueError, match='.*?too long.*?'):
            User.get_user_by_login(user_name='123' * 100, password=testPassword)


def test_updateUser(app):
    with app.app_context():
        testUser = User.get_user_by_login(user_name=testUsername, password=testPassword)
        assert testUser.first_name is None
        assert testUser.last_name is None
        assert testUser.email is None
        assert testUser.phone is None

        # Update user's profile
        dataMap = {
            'first_name': 'Linbin',
            'last_name': 'Pang',
            'email': 'i@teenet.me',
            'phone': '1231231223'
        }
        testUser.update_user_by_data_map(dataMap)

        testUser = User.get_user_by_login(user_name=testUsername, password=testPassword)
        assert testUser.first_name == dataMap['first_name']
        assert testUser.last_name == dataMap['last_name']
        assert testUser.email == dataMap['email']
        assert testUser.phone == dataMap['phone']


        # Update user's password
        dataMap = {
            'password': 'newpassword'
        }
        alteredPassword = dataMap['password']
        testUser.update_user_by_data_map(dataMap)
        with pytest.raises(ValueError, match='.*?incorrect.*?'):
            User.get_user_by_login(user_name=testUsername, password=testPassword)

        dataMap = {
            'password': 'newpa'
        }
        with pytest.raises(ValueError, match='.*?too short.*?'):
            testUser.update_user_by_data_map(dataMap)

        dataMap = {
            'password': 'newpa' * 100
        }
        with pytest.raises(ValueError, match='.*?too long.*?'):
            testUser.update_user_by_data_map(dataMap)

        # update user's name
        dataMap = {
            'username': testAnotherUsername
        }
        alteredUsername = dataMap['username']
        testUser.update_user_by_data_map(dataMap)
        with pytest.raises(ValueError, match='.*?already been used.*?'):
            testUser.update_user_by_data_map(dataMap)

        testUser = User.get_user_by_login(user_name=alteredUsername, password=alteredPassword)
        assert isinstance(testUser, User)




def test_end(app):
    with app.app_context():
        User.delete_user(user_name=testUsername)
        User.delete_user(user_name=testAnotherUsername)
        stop_jwt_activity_manager_thread()
