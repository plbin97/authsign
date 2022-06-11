import _thread
from typing import Dict
from datetime import datetime
import shortuuid

jwtIDuserIDMaps: Dict[str: dict] = {}


def checkingForjwtIDexpiration():
    while True:
        now = datetime.utcnow()
        for jwtID in jwtIDuserIDMaps:
            jwtIDuserIDMap = jwtIDuserIDMaps[jwtID]
