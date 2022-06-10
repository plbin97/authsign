import hashlib


def hashPassword(password: str) -> str:
    """
    Hash the password into a string with length of 32
    :param password:
    :return:
    """
    return hashlib.md5(password.encode()).hexdigest()
