import asyncio
from threading import Thread

activeJwtHash = []
running = True
eventLoop: asyncio.AbstractEventLoop or None = None
eventLoopThread: Thread or None


def startJwtActivityManagerThread():
    """
    Start the thread
    :return:
    """
    global eventLoop
    global eventLoopThread
    global running
    global activeJwtHash
    eventLoop = asyncio.get_event_loop()
    running = True
    activeJwtHash = []
    eventLoopThread = Thread(target=_loopInThread, args=())
    eventLoopThread.setDaemon(True)
    eventLoopThread.start()


def stopJwtActivityManagerThread():
    """
    Stop the thread
    For testing
    :return:
    """
    global running
    running = False
    eventLoopThread.join()


async def _emptyCoroutine():
    """
    An empty forever running coroutine
    :return:
    """
    while running:
        await asyncio.sleep(1)


async def _newActiveJwtHashRemover(jwtHash: int, countDown: int):
    """
    Coroutine for remove the jwt hash in future
    :param jwtHash:
    :param countDown:
    :return:
    """
    await asyncio.sleep(countDown)
    if jwtHash in activeJwtHash:
        activeJwtHash.remove(jwtHash)


def _loopInThread():
    """
    This method would be run in a thread for start up the event loop
    :param loop:
    :return:
    """
    global eventLoop
    asyncio.set_event_loop(eventLoop)

    eventLoop.run_until_complete(_emptyCoroutine())


def activateJwt(jwtHash: int, expiredInSec: int = 7200):
    """
    Activate a Jwt; after 'expiredInSec', the Jwt would be non-active
    :param jwtHash:
    :param expiredInSec:
    :return:
    """
    activeJwtHash.append(jwtHash)
    asyncio.set_event_loop(eventLoop)
    asyncio.ensure_future(_newActiveJwtHashRemover(jwtHash, expiredInSec))


def isJwtActive(jwtHash: int) -> bool:
    """
    Check if Jwt string is active
    :param jwtHash:
    :return:
    """
    return jwtHash in activeJwtHash


def disableJwt(jwtHash: int):
    """
    Disable a JWT, make it expired
    :param jwtHash:
    :return:
    """
    if jwtHash in activeJwtHash:
        activeJwtHash.remove(jwtHash)
