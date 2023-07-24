import asyncio
import logging.handlers
import sys
import traceback
from io import BytesIO
from sys import platform
from typing import Any
from urllib.request import Request, urlopen

import aiohttp
import discord
from discord import Intents, __version__
from discord.ext import commands
from discord.ext.commands import CommandNotFound

import api
import helper


class Joshy(commands.Bot):
    def __init__(self):
        member_cache_flags = discord.MemberCacheFlags.from_intents(
            discord.Intents.all()
        )
        allowed_mentions = discord.AllowedMentions(
            everyone=False, roles=False, users=True, replied_user=True
        )
        super().__init__(
            max_messages=5000,
            command_prefix=Joshy.my_prefix,
            case_insensitive=True,
            strip_after_prefix=True,
            help_command=None,
            intents=discord.Intents.all(),
            description="Discord Bot",
            chunk_guilds_at_startup=True,
            member_cache_flags=member_cache_flags,
            allowed_mentions=allowed_mentions,
            heartbeat_timeout=150.0,
        )
        self.primary_extensions: list[str] = [
            "cogs.profileviewer",
            # "jishaku",
        ]

        self.creds = helper.load_json("creds", add_config_dir=False)
        self.bot_token = self.creds["token"]
        self.api = self.creds["api_key"]


    async def setup_hook(self) -> None:
        await self.load_extensions()

    async def load_extensions(self):
        for ext in self.primary_extensions:
            try:
                await self.load_extension(ext)
                print(ext)
            except Exception as error:
                traceback.print_tb(error.__traceback__)
                print(error)

    def my_prefix(self, message: discord.Message):
        prefixes = ["^"]
        if not message.guild:
            return "^"
        return commands.when_mentioned_or(*prefixes)(self, message)

    async def on_ready(self):
        print(
            f"\n\nLogged in as: {self.user.name} - {self.user.id}\nVersion: {__version__}\n"
        )
        print("Successfully logged in and booted...!")

    async def run(self, *args: Any, **kwargs: Any) -> None:
        logger = logging.getLogger("discord")
        logger.setLevel(logging.INFO)

        handler = logging.handlers.RotatingFileHandler(
            filename="discord.log",
            encoding="utf-8",
            maxBytes=32 * 1024 * 1024,  # 32 MiB
            backupCount=5,  # Rotate through 5 files
        )
        dt_fmt = "%Y-%m-%d %H:%M:%S"
        formatter = logging.Formatter(
            "[{asctime}] [{levelname:<8}] {name}: {message}", dt_fmt, style="{"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        if platform == "win32":
            root = logging.getLogger()
            root.setLevel(logging.INFO)

            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(logging.INFO)
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            root.addHandler(handler)

        await super().start(
            self.bot_token,
            reconnect=True,
        )

async def run_bot():
    async with Joshy() as bot:
        await bot.run()

def main():
    asyncio.run(run_bot())

if __name__ == "__main__":
    main()

