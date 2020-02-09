import asyncio


async def compute(task):
    for i in range(task.n):
        await asyncio.sleep(task.interval)

        task.v += task.d
