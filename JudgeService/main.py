import asyncio
import logging
import os


async def main():
    from judgeservice.application import ServerApplication
    app = ServerApplication()
    await app.run()


if __name__ == "__main__":
    _level = logging.DEBUG if os.getenv("DEBUG") is True else logging.INFO
    logging.basicConfig(level=_level, format="(%(asctime)s)\t[%(levelname)s]\t%(message)s")
    asyncio.run(main())

