import asyncio


async def scheduler(func, timeout: float, *args):
    await asyncio.sleep(delay=timeout)

    await func(*args)
