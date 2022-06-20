from src.authsign.databaseModels.User import User

testUsername: str = 'panglinbin'
testPassword: str = 'thisismypassword'


def test_init(newApp):
    pass


def test_newUserPositive(app):
    with app.app_context():
        User.deleteUser(userName=testUsername)
        testUser = User.newUser(userName=testUsername, password=testPassword)
        assert isinstance(testUser, User)


def test_newUserNegative(app):
    with app.app_context():
        errMsg = User.newUser(userName=testUsername, password=testPassword)
        assert isinstance(errMsg, str)
        errMsg = User.newUser(userName=testUsername, password='123')
        assert isinstance(errMsg, str)
        errMsg = User.newUser(userName='123', password=testPassword)
        assert isinstance(errMsg, str)
        errMsg = User.newUser(userName='123' * 100, password=testPassword)
        assert isinstance(errMsg, str)
        errMsg = User.newUser(userName=testUsername, password='123' * 100)
        assert isinstance(errMsg, str)


def test_loginUserPositive(app):
    with app.app_context():
        testUser = User.getUserByLogin(userName=testUsername, password=testPassword)
        assert isinstance(testUser, User)


def test_loginUserNegative(app):
    with app.app_context():
        errMsg = User.getUserByLogin(userName='123', password=testPassword)
        assert isinstance(errMsg, str)
        errMsg = User.getUserByLogin(userName=testUsername, password='123')
        assert isinstance(errMsg, str)
        errMsg = User.getUserByLogin(userName='123' * 100, password=testPassword)
        assert isinstance(errMsg, str)
        errMsg = User.getUserByLogin(userName=testUsername, password='123' * 100)
        assert isinstance(errMsg, str)


def test_deleteUser(app):
    with app.app_context():
        User.deleteUser(userName=testUsername)
