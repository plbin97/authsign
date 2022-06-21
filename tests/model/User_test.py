import pytest

from src.authsign.databaseModels.User import User
from src.authsign.utils.jwt import stopJwtActivityManagerThread

testUsername: str = 'panglinbin'
testAnotherUsername: str = 'linbinpang'
testPassword: str = 'thisismypassword'


def test_init(newApp):
    with newApp.app_context():
        User.deleteUser(userName=testUsername)
        User.deleteUser(userName=testAnotherUsername)


def test_newUser(app):
    with app.app_context():
        testUser = User.newUser(userName=testUsername, password=testPassword)
        assert isinstance(testUser, User)

        with pytest.raises(ValueError, match='.*?been used.*?'):
            User.newUser(userName=testUsername, password=testPassword)

        with pytest.raises(ValueError, match='.*?too short.*?'):
            User.newUser(userName='otherUsernameTest', password='123')

        with pytest.raises(ValueError, match='.*?too short.*?'):
            User.newUser(userName='123', password=testPassword)

        with pytest.raises(ValueError, match='.*?too long.*?'):
            User.newUser(userName='123' * 100, password=testPassword)

        with pytest.raises(ValueError, match='.*?too long.*?'):
            User.newUser(userName='otherUsernameTest', password='123' * 100)


def test_loginUser(app):
    with app.app_context():
        testUser = User.getUserByLogin(userName=testUsername, password=testPassword)
        assert isinstance(testUser, User)
        with pytest.raises(ValueError, match='.*?incorrect.*?'):
            User.getUserByLogin(userName='123', password=testPassword)
        with pytest.raises(ValueError, match='.*?incorrect.*?'):
            User.getUserByLogin(userName=testUsername, password='123')
        with pytest.raises(ValueError, match='.*?too long.*?'):
            User.getUserByLogin(userName=testUsername, password='123' * 100)
        with pytest.raises(ValueError, match='.*?too long.*?'):
            User.getUserByLogin(userName='123' * 100, password=testPassword)


def test_updateUser(app):
    with app.app_context():
        testUser = User.getUserByLogin(userName=testUsername, password=testPassword)
        assert testUser.firstName is None
        assert testUser.lastName is None
        assert testUser.email is None
        assert testUser.phone is None

        # Update user's profile
        dataMap = {
            'firstName': 'Linbin',
            'lastName': 'Pang',
            'email': 'i@teenet.me',
            'phone': '1231231223'
        }
        testUser.updateUserByDataMap(dataMap)

        testUser = User.getUserByLogin(userName=testUsername, password=testPassword)
        assert testUser.firstName == dataMap['firstName']
        assert testUser.lastName == dataMap['lastName']
        assert testUser.email == dataMap['email']
        assert testUser.phone == dataMap['phone']


        # Update user's password
        dataMap = {
            'password': 'newpassword'
        }
        alteredPassword = dataMap['password']
        testUser.updateUserByDataMap(dataMap)
        with pytest.raises(ValueError, match='.*?incorrect.*?'):
            User.getUserByLogin(userName=testUsername, password=testPassword)

        dataMap = {
            'password': 'newpa'
        }
        with pytest.raises(ValueError, match='.*?too short.*?'):
            testUser.updateUserByDataMap(dataMap)

        dataMap = {
            'password': 'newpa' * 100
        }
        with pytest.raises(ValueError, match='.*?too long.*?'):
            testUser.updateUserByDataMap(dataMap)

        # update user's name
        dataMap = {
            'username': testAnotherUsername
        }
        alteredUsername = dataMap['username']
        testUser.updateUserByDataMap(dataMap)
        with pytest.raises(ValueError, match='.*?already been used.*?'):
            testUser.updateUserByDataMap(dataMap)

        testUser = User.getUserByLogin(userName=alteredUsername, password=alteredPassword)
        assert isinstance(testUser, User)




def test_end(app):
    with app.app_context():
        User.deleteUser(userName=testUsername)
        User.deleteUser(userName=testAnotherUsername)
        stopJwtActivityManagerThread()
