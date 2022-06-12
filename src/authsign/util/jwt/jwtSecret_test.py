from .jwtSecret import jwtSecret


def test():
    assert len(jwtSecret) > 0
