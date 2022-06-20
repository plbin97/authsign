from src.authsign.utils.jwt.jwtSecret import jwtSecret


def test():
    assert len(jwtSecret) > 0
