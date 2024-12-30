import logging
from pathlib import Path
from typing import Any, Dict

from typing_extensions import override

try:
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
    from apscheduler.schedulers.background import BackgroundScheduler
    from discord import Bot
except ImportError as exc:
    raise ImportError("You need to install libbot[pycord] in order to use this class.") from exc

try:
    from ujson import loads
except ImportError:
    from json import loads

from ...i18n.classes import BotLocale

logger = logging.getLogger(__name__)


class PycordBot(Bot):
    @override
    def __init__(
        self,
        *args,
        config: Dict[str, Any] | None = None,
        config_path: str | Path = Path("config.json"),
        locales_root: str | Path | None = None,
        scheduler: AsyncIOScheduler | BackgroundScheduler | None = None,
        **kwargs,
    ):
        if config is None:
            with open(config_path, "r", encoding="utf-8") as f:
                self.config: dict = loads(f.read())
        else:
            self.config = config

        super().__init__(
            debug_guilds=(self.config["bot"]["debug_guilds"] if self.config["debug"] else None),
            owner_ids=self.config["bot"]["owners"],
            *args,
            **kwargs,
        )

        self.bot_locale: BotLocale = BotLocale(
            default_locale=self.config["locale"],
            locales_root=(Path("locale") if locales_root is None else locales_root),
        )
        self.default_locale: str = self.bot_locale.default
        self.locales: Dict[str, Any] = self.bot_locale.locales

        self._ = self.bot_locale._
        self.in_all_locales = self.bot_locale.in_all_locales
        self.in_every_locale = self.bot_locale.in_every_locale

        self.scheduler: AsyncIOScheduler | BackgroundScheduler | None = scheduler

    @override
    async def start(self, token: str, reconnect: bool = True, scheduler_start: bool = True) -> None:
        if self.scheduler is not None and scheduler_start:
            self.scheduler.start()

        await super().start(token, reconnect=reconnect)

    @override
    async def close(self, scheduler_shutdown: bool = True, scheduler_wait: bool = True) -> None:
        if self.scheduler is not None and scheduler_shutdown:
            self.scheduler.shutdown(scheduler_wait)

        await super().close()
