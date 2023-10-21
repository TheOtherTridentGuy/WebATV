# pylint: disable-all
import pyatv
import asyncio


async def main():
    for result in await pyatv.scan(asyncio.get_event_loop()):
        print(result)
        conn = await pyatv.connect(result, asyncio.get_event_loop())
        print(conn)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
