import asyncio

from judgeservice.application import ServerApplication


async def main():
    app = ServerApplication(config_path="../config.yml")
    await app.run()


if __name__ == "__main__":
    asyncio.run(main())
