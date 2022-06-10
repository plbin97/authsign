from .jwtVerifier import jwtEncode, jwtSecret, jwtDecode
from datetime import datetime, timedelta

def test():
    testID = 1234
    testRole = 1
    assert jwtSecret is not None
    assert len(jwtSecret) > 0
    encodedStr = jwtEncode(testID, testRole, 2)
    assert encodedStr is not None
    assert len(encodedStr) > 0
    decodedID, decodedRole = jwtDecode(encodedStr)
    assert decodedID == testID
    assert decodedRole == testRole
    expiredDecoded = jwtDecode(encodedStr, datetime.utcnow() + timedelta(days=1))
    assert expiredDecoded[0] is None
    assert expiredDecoded[1] is None
    errorDecoded = jwtDecode('12345', datetime.utcnow() + timedelta(days=1))
    assert errorDecoded[0] is None
    assert errorDecoded[1] is None
