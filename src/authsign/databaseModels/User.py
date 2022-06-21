from ..extension import db
from ..utils import hashPassword


class User(db.Model):
    """
    Value error would be raised if the parameters are invalid.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    firstName = db.Column(db.String(64), nullable=True)
    lastName = db.Column(db.String(64), nullable=True)
    email = db.Column(db.String(64), nullable=True)
    emailVerified = db.Column(db.Boolean, nullable=False)
    password = db.Column(db.String(32), nullable=False)
    phone = db.Column(db.String(32), nullable=True)
    role = db.Column(db.Integer, nullable=False)

    def __init__(self, username: str, password: str):
        self.setUsername(username)
        self.setPassword(password)
        self.emailVerified = False
        self.role = 1

    def setUsername(self, username: str):
        if len(username) < 4:
            raise ValueError('Your username is too short')
        if len(username) > 32:
            raise ValueError('Your username is too long')
        user: User = User.query.filter_by(username=username).first()
        if user is not None:
            raise ValueError('Your username has already been used')
        self.username = username

    def setPassword(self, password: str):
        if len(password) < 6:
            raise ValueError('Your password is too short')
        if len(password) > 32:
            raise ValueError('Your password is too long')
        self.password = hashPassword(password)

    def setFirstName(self, firstName: str):
        if len(firstName) > 64:
            raise ValueError('Your first name is too long')
        self.firstName = firstName

    def setLastName(self, lastName: str):
        if len(lastName) > 64:
            raise ValueError('Your last name is too long')
        self.lastName = lastName

    def setPhone(self, phoneNumber: str):
        if len(phoneNumber) > 32:
            raise ValueError('Your phone number is too long')
        self.phone = phoneNumber

    def setEmail(self, email: str):
        if len(email) > 64:
            raise ValueError('Your email is too long')
        self.email = email

    def __repr__(self) -> str:
        return '<User %r>' % self.username

    def isAdmin(self) -> bool:
        """
        Check if user is admin
        :return:
        """
        return self.role == 0

    def toDict(self) -> dict:
        """
        Translate the object into a dictionary
        :return:
        """
        userDict: dict = self.__dict__
        del userDict['_sa_instance_state']
        userDict['password'] = ''
        return userDict

    def updateUserByDataMap(self, dataMap: dict):
        for keyInReq in dataMap:
            if hasattr(self, keyInReq):
                data = dataMap[keyInReq]
                if keyInReq == 'username':
                    self.setUsername(data)
                    continue
                if keyInReq == 'password':
                    self.setPassword(data)
                    continue
                if keyInReq == 'firstName':
                    self.setFirstName(data)
                    continue
                if keyInReq == 'lastName':
                    self.setLastName(data)
                    continue
                if keyInReq == 'email':
                    self.setEmail(data)
                    continue
                if keyInReq == 'phone':
                    self.setPhone(data)
                    continue
        db.session.commit()

    @classmethod
    def getUserByLogin(cls, userName: str, password: str):
        """
        For login
        :param userName:
        :param password:
        :return:
        User if login successful
        """
        if len(userName) > 32:
            raise ValueError('Username is too long')
        if len(password) > 32:
            raise ValueError('Password is too long')

        hashedPassword: str = hashPassword(password)
        user: cls = cls.query.filter_by(username=userName, password=hashedPassword).first()

        if user is None:
            raise ValueError('Username or password incorrect')
        return user

    @classmethod
    def newUser(cls, userName: str, password: str):
        """
        For new user sign up
        :param userName:
        :param password:
        :return:
        User
        """

        newUser: cls = cls(username=userName, password=password)
        db.session.add(newUser)
        db.session.commit()
        return newUser

    @classmethod
    def deleteUser(cls, userName: str):
        """
        Delete user
        :param userName:
        :return:
        """
        user: cls = cls.query.filter_by(username=userName).first()
        if user is not None:
            db.session.delete(user)
            db.session.commit()
