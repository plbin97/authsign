from src.authsign.utils.hash_password import hash_password

def test():
    hashed: str = hash_password('123')
    assert len(hashed) == 32