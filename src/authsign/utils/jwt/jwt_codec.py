"""
Module for encoding and decoding the JWT
"""
from datetime import datetime, timedelta
from random import randrange
import jwt
from .jwt_secret import JWT_SECRET


class JwtCodec:
    """
    For encoding and decoding the JWT
    """
    user_id: int
    utc_time_of_issue: datetime
    utc_time_of_expire: datetime
    jwt_id: int
    role: int
    jwt_temp: str = ''

    def __init__(
            self,
            user_id: int,
            utc_time_of_issue: datetime,
            utc_time_of_expire: datetime,
            role: int,
            jwt_id: int
    ):
        # pylint: disable=too-many-arguments
        self.user_id = user_id
        self.utc_time_of_issue = utc_time_of_issue
        self.utc_time_of_expire = utc_time_of_expire
        self.role = role
        self.jwt_id = jwt_id

    @classmethod
    def from_jwt_str(cls, jwt_encoded_str: str):
        """
        Constructor that create the object by JWT string
        :param jwt_encoded_str:
        :return:
        """
        try:
            jwt_payload: dict = jwt.decode(jwt_encoded_str, JWT_SECRET, algorithms='HS256')
        except jwt.exceptions.InvalidTokenError:
            return None

        user_id = jwt_payload['user_id']
        utc_time_of_issue = datetime.strptime(jwt_payload['utc_time_of_issue'], '%c')
        utc_time_of_expire = datetime.strptime(jwt_payload['utc_time_of_expire'], '%c')
        role = jwt_payload['role']
        jwt_id = jwt_payload['jwt_id']
        return cls(
            user_id=user_id,
            utc_time_of_issue=utc_time_of_issue,
            utc_time_of_expire=utc_time_of_expire,
            role=role,
            jwt_id=jwt_id
        )

    @classmethod
    def new_jwt(
            cls,
            user_id: int,
            utc_time_of_issue: datetime = datetime.utcnow(),
            utc_time_of_expire: datetime = datetime.utcnow() + timedelta(hours=2),
            role: int = 0
    ):
        """
        Create a new JwtCodec
        :param user_id:
        :param utc_time_of_issue:
        :param utc_time_of_expire:
        :param role:
        :return:
        """
        return cls(
            user_id=user_id,
            utc_time_of_issue=utc_time_of_issue,
            utc_time_of_expire=utc_time_of_expire,
            role=role,
            jwt_id=randrange(0, 999999)
        )

    def is_expired(self) -> bool:
        """
        Check if jwt is expired
        :return:
        True if expired
        """
        now: datetime = datetime.utcnow()
        return self.utc_time_of_expire < now

    def get_jwt_str(self) -> str:
        """
        Encode the data into Jwt string
        :return:
        """
        if self.jwt_temp != '':
            return self.jwt_temp
        jwt_payload: dict = {
            'utc_time_of_issue': self.utc_time_of_issue.strftime('%c'),
            'utc_time_of_expire': self.utc_time_of_expire.strftime('%c'),
            'user_id': self.user_id,
            'role': self.role,
            'jwt_id': self.jwt_id
        }
        self.jwt_temp = jwt.encode(jwt_payload, JWT_SECRET, 'HS256')
        return self.jwt_temp

    def get_jwt_hash(self) -> int:
        """
        Get the hash of JWT
        :return:
        """
        if self.jwt_temp != '':
            return hash(self.jwt_temp)
        return hash(self.get_jwt_str())
