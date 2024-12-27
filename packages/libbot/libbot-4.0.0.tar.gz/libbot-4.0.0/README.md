<h1 align="center">LibBotUniversal</h1>

<p align="center">
<a href="https://git.end-play.xyz/profitroll/LibBotUniversal/src/branch/master/LICENSE"><img alt="PyPI - License" src="https://img.shields.io/pypi/l/libbot">
<a href="https://git.end-play.xyz/profitroll/LibBotUniversal/releases/latest"><img alt="Gitea Release" src="https://img.shields.io/gitea/v/release/profitroll/LibBotUniversal?gitea_url=https%3A%2F%2Fgit.end-play.xyz"></a>
<a href="https://pypi.org/project/libbot/"><img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/libbot"></a>
<a href="https://git.end-play.xyz/profitroll/LibBotUniversal"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>  

Handy library for Telegram/Discord bots development.

## Getting started

There are different sub-packages available:

* pyrogram - Telegram bots with Pyrogram's fork "Pyrofork"
* pycord - Discord bots with Pycord
* speed - Performance improvements
* dev - Dependencies for package development purposes

You can freely choose any sub-package you want, as well as add multiple (comma-separated) or none at all.

```shell
# Only general features
pip install libbot

# Only with Pyrogram
pip install libbot[pyrogram]

# With Pycord and Performance improvements
pip install libbot[pycord,speed]
```

## Examples

### Pyrogram

```python
from libbot.pyrogram import PyroClient

def main():
    client = PyroClient(scheduler=scheduler)

    try:
        client.run()
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        if client.scheduler is not None:
            client.scheduler.shutdown()
        exit()


if __name__ == "__main__":
    main()
```

### Pycord

```python
from discord import Intents
from libbot import sync
from libbot.pycord import PycordBot


async def main():
    intents = Intents.default()
    bot = PycordBot(intents=intents)

    bot.load_extension("cogs")

    try:
        await bot.start(sync.config_get("bot_token", "bot"))
    except KeyboardInterrupt:
        logger.warning("Shutting down...")
        await bot.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
```

## Config examples

For bot config examples please check the examples directory. Without a valid config file, the bot won't start at all, so you need to make sure the correct config file is used.
