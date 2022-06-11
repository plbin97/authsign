import asyncio
async def greet_every_1_seconds():
    while True:
        print('Hello')
        await asyncio.sleep(1)

def runAnohter():
    asyncio.ensure_future(greet_every_1_seconds())