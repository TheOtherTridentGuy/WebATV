# pylint: disable-all
import pyatv
import asyncio


async def main():
    for result in await pyatv.scan:
        print(result)


asyncio.run(asyncio.coroutine(main))
