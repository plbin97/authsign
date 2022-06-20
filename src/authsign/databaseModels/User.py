from ..extension import db
from ..utils import hashPassword


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    firstName = db.Column(db.String(64), nullable=True)
    lastName = db.Column(db.String(64), nullable=True)
    email = db.Column(db.String(64), nullable=True)
    emailVerified = db.Column(db.Boolean, nullable=False)
    password = db.Column(db.String(32), nullable=False)
    phone = db.Column(db.String(32), nullable=True)
    role = db.Column(db.Integer, nullable=False)

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

    def userUpdateInfo(self, mapOfData: dict):
        for keyInReq in mapOfData:
            if hasattr(self, keyInReq):
                if isinstance(mapOfData[keyInReq], type(getattr(self, keyInReq))):
                    if keyInReq == 'password':
                        self.password = hashPassword(mapOfData[keyInReq])
                    else:
                        setattr(self, keyInReq, mapOfData[keyInReq])

        db.session.commit()

    @classmethod
    def getUserByLogin(cls, userName: str, password: str):
        """
        For login
        :param userName:
        :param password:
        :return:
        string if invalid input
        User if login successful
        """
        if len(userName) > 32:
            return 'Username is too long'
        if len(password) > 32:
            return 'Password is too long'

        hashedPassword: str = hashPassword(password)
        user: cls = cls.query.filter_by(username=userName, password=hashedPassword).first()

        if user is None:
            return 'Username or password incorrect'
        return user


    @classmethod
    def newUser(cls, userName: str, password: str):
        """
        For new user sign up
        :param userName:
        :param password:
        :return:
        string if invalid input
        User if successfully create a new user
        """
        if len(userName) < 4:
            return 'Your username is too short'
        if len(userName) > 32:
            return 'Your username is too long'
        if len(password) < 6:
            return 'Your password is too short'
        if len(password) > 32:
            return 'Your password is too long'

        if cls.query.filter_by(username=userName).first() is not None:
            return 'Your username has already been used'

        passwordHash: str = hashPassword(password)
        newUser: cls = cls(username=userName, password=passwordHash, emailVerified=False, role=1)
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
