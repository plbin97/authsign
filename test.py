import asyncio
import time
import threading
import anotherTest


async def greet_every_two_seconds():
    while True:
        await asyncio.sleep(2)


def loop_in_thread(loop):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(greet_every_two_seconds())

loop = asyncio.get_event_loop()

t = threading.Thread(target=loop_in_thread, args=(loop,))

t.start()
print(threading.active_count())
anotherTest.runAnohter()
print(threading.active_count())
anotherTest.runAnohter()
print(threading.active_count())