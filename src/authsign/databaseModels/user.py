"""User model"""
from ..extension import db
from ..utils import hash_password


class User(db.Model):
    """
    Value error would be raised if the parameters are invalid.
    """
    # pylint: disable=too-many-instance-attributes
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    first_name = db.Column(db.String(64), nullable=True)
    last_name = db.Column(db.String(64), nullable=True)
    email = db.Column(db.String(64), nullable=True)
    email_verified = db.Column(db.Boolean, nullable=False)
    password = db.Column(db.String(32), nullable=False)
    phone = db.Column(db.String(32), nullable=True)
    role = db.Column(db.Integer, nullable=False)

    def __init__(self, username: str, password: str):
        self.set_username(username)
        self.set_password(password)
        self.email_verified = False
        self.role = 1

    def set_username(self, username: str):
        """
        Set user name
        :param username: str
        :return: void
        """
        if len(username) < 4:
            raise ValueError('Your username is too short')
        if len(username) > 32:
            raise ValueError('Your username is too long')
        user: User = User.query.filter_by(username=username).first()
        if user is not None:
            raise ValueError('Your username has already been used')
        self.username = username

    def set_password(self, password: str):
        """
        Set password
        :param password: str
        :return: void
        """
        if len(password) < 6:
            raise ValueError('Your password is too short')
        if len(password) > 32:
            raise ValueError('Your password is too long')
        self.password = hash_password(password)

    def set_first_name(self, first_name: str):
        """
        Set first name
        :param first_name: str
        :return: void
        """
        if len(first_name) > 64:
            raise ValueError('Your first name is too long')
        self.first_name = first_name

    def set_last_name(self, last_name: str):
        """
        Set last name
        :param last_name: str
        :return: void
        """
        if len(last_name) > 64:
            raise ValueError('Your last name is too long')
        self.last_name = last_name

    def set_phone(self, phone_number: str):
        """
        Set phone number
        :param phone_number: str
        :return: void
        """
        if len(phone_number) > 32:
            raise ValueError('Your phone number is too long')
        self.phone = phone_number

    def set_email(self, email: str):
        """
        Set email
        :param email: str
        :return: void
        """
        if len(email) > 64:
            raise ValueError('Your email is too long')
        self.email = email

    def __repr__(self) -> str:
        return self.username

    def is_admin(self) -> bool:
        """
        Check if user is admin
        :return:
        """
        return self.role == 0

    def to_dict(self) -> dict:
        """
        Translate the object into a dictionary
        :return:
        """
        user_dict: dict = self.__dict__
        del user_dict['_sa_instance_state']
        user_dict['password'] = ''
        return user_dict

    def update_user_by_data_map(self, data_map: dict):
        """
        Update user by data from request body
        :param data_map: request data body
        :return: void
        """
        for key_in_req in data_map:
            if hasattr(self, key_in_req):
                data = data_map[key_in_req]
                if key_in_req == 'username':
                    self.set_username(data)
                    continue
                if key_in_req == 'password':
                    self.set_password(data)
                    continue
                if key_in_req == 'first_name':
                    self.set_first_name(data)
                    continue
                if key_in_req == 'last_name':
                    self.set_last_name(data)
                    continue
                if key_in_req == 'email':
                    self.set_email(data)
                    continue
                if key_in_req == 'phone':
                    self.set_phone(data)
                    continue
        db.session.commit()

    @classmethod
    def get_user_by_login(cls, user_name: str, password: str):
        """
        For signin
        :param user_name:
        :param password:
        :return:
        User if signin successful
        """
        if len(user_name) > 32:
            raise ValueError('Username is too long')
        if len(password) > 32:
            raise ValueError('Password is too long')

        hashed_password: str = hash_password(password)
        user: cls = cls.query.filter_by(username=user_name, password=hashed_password).first()

        if user is None:
            raise ValueError('Username or password incorrect')
        return user

    @classmethod
    def new_user(cls, user_name: str, password: str):
        """
        For new user sign up
        :param user_name:
        :param password:
        :return:
        User
        """

        new_user: cls = cls(username=user_name, password=password)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @classmethod
    def delete_user(cls, user_name: str):
        """
        Delete user
        :param user_name:
        :return:
        """
        user: cls = cls.query.filter_by(username=user_name).first()
        if user is not None:
            db.session.delete(user)
            db.session.commit()
