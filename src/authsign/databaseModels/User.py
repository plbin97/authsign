from ..extension import db
from ..util import hashPassword


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
