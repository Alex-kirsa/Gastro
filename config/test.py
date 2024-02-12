import asyncio
from random import randint


async def foo():
    await asyncio.sleep(randint(1, 5))
    print("ASD")


# for _ in range(10):
#    loop = asyncio.get_event_loop()
#    loop.create_task(foo())
#
# loop.run_until_complete()


async def run_test():
    loop = asyncio.get_event_loop()
    tasks = []
    for _ in range(10):
        task = loop.create_task(foo())
        tasks.append(task)
    await asyncio.gather(*tasks)


asyncio.run(run_test())
