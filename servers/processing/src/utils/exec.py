import asyncio


async def run_in_executor(executor, func, *args):
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(executor, func, *args)
    return result