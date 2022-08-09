"""
Module for managing and storing the JWT data in memory
"""
# pylint: disable=W0603
import asyncio
from threading import Thread

ACTIVE_JWT_HASH = []
RUNNING = True
EVENT_LOOP: asyncio.AbstractEventLoop or None = None
EVENT_LOOP_THREAD: Thread or None


def start_jwt_activity_manager_thread():
    """
    Start the thread
    :return:
    """
    global EVENT_LOOP
    global EVENT_LOOP_THREAD
    global RUNNING
    global ACTIVE_JWT_HASH
    EVENT_LOOP = asyncio.get_event_loop()
    RUNNING = True
    ACTIVE_JWT_HASH = []
    EVENT_LOOP_THREAD = Thread(target=_loop_in_thread, args=())
    EVENT_LOOP_THREAD.daemon = True
    EVENT_LOOP_THREAD.start()


def stop_jwt_activity_manager_thread():
    """
    Stop the thread
    For testing
    :return:
    """
    global RUNNING
    RUNNING = False
    EVENT_LOOP_THREAD.join()


async def _empty_coroutine():
    """
    An empty forever RUNNING coroutine
    :return:
    """
    while RUNNING:
        await asyncio.sleep(1)


async def _new_active_jwt_hash_remover(jwt_hash: int, count_down: int):
    """
    Coroutine for remove the jwt hash in future
    :param jwt_hash:
    :param count_down:
    :return:
    """
    await asyncio.sleep(count_down)
    if jwt_hash in ACTIVE_JWT_HASH:
        ACTIVE_JWT_HASH.remove(jwt_hash)


def _loop_in_thread():
    """
    This method would be run in a thread for start up the event loop
    :param loop:
    :return:
    """
    asyncio.set_event_loop(EVENT_LOOP)

    EVENT_LOOP.run_until_complete(_empty_coroutine())


def activate_jwt(jwt_hash: int, expired_in_sec: int = 7200):
    """
    Activate a Jwt; after 'expired_in_sec', the Jwt would be non-active
    :param jwt_hash:
    :param expired_in_sec:
    :return:
    """
    ACTIVE_JWT_HASH.append(jwt_hash)
    asyncio.set_event_loop(EVENT_LOOP)
    asyncio.ensure_future(_new_active_jwt_hash_remover(jwt_hash, expired_in_sec))


def is_jwt_active(jwt_hash: int) -> bool:
    """
    Check if Jwt string is active
    :param jwt_hash:
    :return:
    """
    return jwt_hash in ACTIVE_JWT_HASH


def disable_jwt(jwt_hash: int):
    """
    Disable a JWT, make it expired
    :param jwt_hash:
    :return:
    """
    if jwt_hash in ACTIVE_JWT_HASH:
        ACTIVE_JWT_HASH.remove(jwt_hash)
