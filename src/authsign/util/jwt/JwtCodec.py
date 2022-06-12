from datetime import datetime, timedelta
import jwt
from .jwtSecret import jwtSecret


class JwtCodec:
    userID: int
    utcTimeOfIssue: datetime
    utcTimeOfExpire: datetime
    role: int
    jwtTemp: str = ''

    def __init__(
            self,
            userID: int,
            utcTimeOfIssue: datetime,
            utcTimeOfExpire: datetime,
            role: int,
    ):
        self.userID = userID
        self.utcTimeOfIssue = utcTimeOfIssue
        self.utcTimeOfExpire = utcTimeOfExpire
        self.role = role

    @classmethod
    def fromJwtStr(cls, jwtEncodedStr: str):
        """
        Constructor that create the object by JWT string
        :param jwtEncodedStr:
        :return:
        """
        try:
            jwtPayload: dict = jwt.decode(jwtEncodedStr, jwtSecret, algorithms='HS256')
        except:
            return None

        userID = jwtPayload['userID']
        utcTimeOfIssue = datetime.strptime(jwtPayload['utcTimeOfIssue'], '%c')
        utcTimeOfExpire = datetime.strptime(jwtPayload['utcTimeOfExpire'], '%c')
        role = jwtPayload['role']
        return cls(userID=userID, utcTimeOfIssue=utcTimeOfIssue, utcTimeOfExpire=utcTimeOfExpire, role=role)

    @classmethod
    def newJwt(
            cls,
            userID: int,
            utcTimeOfIssue: datetime = datetime.utcnow(),
            utcTimeOfExpire: datetime = datetime.utcnow() + timedelta(hours=2),
            role: int = 0
    ):
        return cls(
            userID=userID,
            utcTimeOfIssue=utcTimeOfIssue,
            utcTimeOfExpire=utcTimeOfExpire,
            role=role,
        )

    def isExpired(self) -> bool:
        """
        Check if jwt is expired
        :return:
        True if expired
        """
        now: datetime = datetime.utcnow()
        return self.utcTimeOfExpire < now

    def getJwtStr(self) -> str:
        """
        Encode the data into Jwt string
        :return:
        """
        if self.jwtTemp != '':
            return self.jwtTemp
        jwtPayload: dict = {
            'utcTimeOfIssue': self.utcTimeOfIssue.strftime('%c'),
            'utcTimeOfExpire': self.utcTimeOfExpire.strftime('%c'),
            'userID': self.userID,
            'role': self.role
        }
        self.jwtTemp = jwt.encode(jwtPayload, jwtSecret, 'HS256')
        return self.jwtTemp

    def getJwtHash(self) -> int:
        """
        Get the hash of JWT
        :return:
        """
        if self.jwtTemp != '':
            return hash(self.jwtTemp)
        return hash(self.getJwtStr())
