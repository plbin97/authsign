import asyncio
import threading

_activeJwtHash = []
_running = True


def stopThread():
    """
    Stop the thread
    For testing
    :return:
    """
    global _running
    _running = False


async def _emptyCoroutine():
    """
    An empty forever running coroutine
    :return:
    """
    while _running:
        await asyncio.sleep(1)


async def _newActiveJwtHashRemover(jwtHash: int, countDown: int):
    """
    Coroutine for remove the jwt hash in future
    :param jwtHash:
    :param countDown:
    :return:
    """
    await asyncio.sleep(countDown)
    _activeJwtHash.remove(jwtHash)


def _loopInThread(eventLoop: asyncio.AbstractEventLoop):
    """
    This method would be run in a thread for start up the event loop
    :param loop:
    :return:
    """
    asyncio.set_event_loop(eventLoop)
    eventLoop.run_until_complete(_emptyCoroutine())  # This will never completed


def activateJwt(jwtHash: int, expiredInSec: int):
    """
    Activate a Jwt; after 'expiredInSec', the Jwt would be non-active
    :param jwtHash:
    :param expiredInSec:
    :return:
    """
    _activeJwtHash.append(jwtHash)
    asyncio.ensure_future(_newActiveJwtHashRemover(jwtHash, expiredInSec))


def isJwtActive(jwtHash: int) -> bool:
    """
    Check if Jwt string is active
    :param jwtHash:
    :return:
    """
    return jwtHash in _activeJwtHash


_eventLoop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
_eventLoopThread = threading.Thread(target=_loopInThread, args=(_eventLoop,))
_eventLoopThread.start()
