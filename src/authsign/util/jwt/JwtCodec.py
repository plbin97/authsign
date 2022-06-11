from datetime import datetime, timedelta
import jwt
from .jwtSecret import jwtSecret
import shortuuid


class JwtCodec:
    userID: int
    jwtID: int
    utcTimeOfIssue: datetime
    utcTimeOfExpire: datetime
    role: int

    def __init__(
            self,
            userID: int,
            utcTimeOfIssue: datetime,
            utcTimeOfExpire: datetime,
            role: int,
            jwtID: int
    ):
        self.userID = userID
        self.jwtID = jwtID
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
        jwtID = jwtPayload['jwtID']
        utcTimeOfIssue = datetime.strptime(jwtPayload['utcTimeOfIssue'], '%c')
        utcTimeOfExpire = datetime.strptime(jwtPayload['utcTimeOfExpire'], '%c')
        role = jwtPayload['role']
        return cls(userID=userID, utcTimeOfIssue=utcTimeOfIssue, utcTimeOfExpire=utcTimeOfExpire, role=role,
                   jwtID=jwtID)

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
            jwtID=shortuuid.uuid()
        )

    def isExpired(self) -> bool:
        """
        Check if jwt is expired
        :return:
        True if expired
        """
        now: datetime = datetime.utcnow()
        return self.utcTimeOfExpire < now

    def encodeToJwtStr(self) -> str:
        """
        Encode the data into Jwt string
        :return:
        """
        jwtPayload: dict = {
            'utcTimeOfIssue': self.utcTimeOfIssue.strftime('%c'),
            'utcTimeOfExpire': self.utcTimeOfExpire.strftime('%c'),
            'jwtID': self.jwtID,
            'userID': self.userID,
            'role': self.role
        }
        return jwt.encode(jwtPayload, jwtSecret, 'HS256')
