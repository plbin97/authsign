from src.authsign.utils.hashPassword import hashPassword

def test():
    hashed: str = hashPassword('123')
    assert len(hashed) == 32