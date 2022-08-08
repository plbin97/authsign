from src.authsign.utils.jwt.jwt_secret import jwtSecret


def test():
    assert len(jwtSecret) > 0
