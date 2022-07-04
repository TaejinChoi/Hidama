# Imports
import os
import hikari
import lightbulb
import aiosqlite

# Random Statuses
from random import choice
from .utilities.randomchoices import statuses

#Bot invocation
bot = lightbulb.BotApp(
    os.environ["TOKEN"],
    default_enabled_guilds=int(os.environ["DEFAULT_GUILD_ID"]),
    help_slash_command=True,
    ignore_bots=True,
    case_insensitive_prefix_commands=True,
    intents=hikari.Intents.ALL,
    prefix=(os.environ["PREFIX"]),
    logs={
        "version": 1,
        "incremental": True,
        "loggers": {
            "hikari": {"level": "INFO"},
            "lightbulb": {"level": "INFO"},
        },
    },
    #owner_ids=(os.environ["OWNERS"]),
)

# Recursive Command Loader

bot.load_extensions_from("./hidama/commands/", must_exist=True, recursive=True)

bot.load_extensions_from("./hidama/helpers/", must_exist=True, recursive=True)

# Something that's needed if you're not on Windows or something?
def run() -> None:
    if os.name != "nt":
        import uvloop
        uvloop.install()

# Turn on Hidama
    bot.run(
        status=hikari.Status.ONLINE,
        activity=hikari.Activity(
            name=choice(statuses),
            type=hikari.ActivityType.WATCHING
        )
    )