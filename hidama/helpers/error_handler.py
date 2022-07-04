#Error handler logic "borrowed" from here. 
#Sorry sorry sorry, but thanks.
#https://github.com/kamfretoz/XJ9/blob/main/meta/error_handler.py
import logging
import lightbulb
import hikari
import random
import datetime
from hidama.utilities.randomchoices import errormsginsert
from hidama.utilities.randomchoices import errormsgimage

error_message = {
    "CommandNotFound": "`{}` is not a command that I can run! Please check my command list for available commands.",
    "MissingPermissions": "You're missing permissions! You need `{}` to run that command!",
    "MissingRequiredArgument": "You are missing 1 or more required arguments: `{}`",
    "CommandOnCooldown": "Cooldown: Wait `{}` seconds.",
    "BotMissingPermissions": "I need more permissions to run this command! Please give me `{}`.",
    "NotOwner": "You can't run this command, stop trying. It only works for my owners.",
    "ConversionError": "Converter failed for `{}`.",
    "NoPrivateMessage": "This is a server only command: It cannot be used in DMs!",
    "NSFWChannelRequired": "Channel needs to be marked NSFW.",
    "CheckFailure": "Command Check Failure: You can't use this command!",
    "ForbiddenError": "Permission forbidden error: I can't perform that action!",
    "ConcurrencyLimit": "Concurrency ratelimit: Wait until the previous command has completed!",
    "BadRequest": "Bad request! Please check your input command for errors!"
}

async def send_embed(name, code, event, *args):
    message = error_message[name]
    if args:
        message = message.format(*args)
    err = hikari.Embed(description=f"**:warning: {message}**", timestamp=datetime.datetime.now().astimezone(), color=0xFF0000)
    if code:
        err.set_image(f"{(random.choice(errormsgimage))}")
    await event.context.respond(content=random.choice(errormsginsert), embed=err)
    
async def on_error(event: lightbulb.CommandErrorEvent) -> None:
    # Unwrap the exception to get the original cause
    exception = event.exception.__cause__ or event.exception
    
    if isinstance(exception, lightbulb.errors.CommandNotFound):
        await send_embed("CommandNotFound", 404, event, exception.invoked_with)
    elif isinstance(exception, lightbulb.errors.MissingRequiredPermission):
        await send_embed("MissingPermissions", 403, event, exception.missing_perms.name)
    elif isinstance(exception, lightbulb.errors.NotEnoughArguments):
        await send_embed("MissingRequiredArgument", 410, event, ", ".join(arg.name for arg in exception.missing_options))
    elif isinstance(exception, lightbulb.CommandIsOnCooldown):
        await send_embed("CommandOnCooldown", 420, event, int(exception.retry_after))
    elif isinstance(exception, lightbulb.errors.BotMissingRequiredPermission):
        await send_embed("BotMissingPermissions", 403, event, exception.missing_perms.name)
    elif isinstance(exception, lightbulb.errors.NotOwner):
        await send_embed("NotOwner", 401, event)
    elif isinstance(exception, lightbulb.errors.ConverterFailure):
        await send_embed("ConversionError", 400, event, exception.option.name)
    elif isinstance(exception, lightbulb.OnlyInGuild):
        await send_embed("NoPrivateMessage", 423, event)
    elif isinstance(exception, lightbulb.errors.NSFWChannelOnly):
        await send_embed("NSFWChannelRequired", 423, event)
    elif isinstance(exception, lightbulb.errors.CheckFailure):
        await send_embed("CheckFailure", 401, event)
    elif isinstance(exception, lightbulb.errors.MaxConcurrencyLimitReached):
        await send_embed("ConcurrencyLimit", 429, event)
    elif isinstance(event.exception.__cause__, hikari.ForbiddenError):
        await send_embed("ForbiddenError", 403, event)
    elif isinstance(event.exception.__cause__, hikari.BadRequestError):
        await send_embed("BadRequest", 400, event)
    else:
        if isinstance(event.exception, lightbulb.CommandInvocationError):
            errormsg = hikari.Embed(title=f"🛑 An error occurred with the `{event.context.command.name}` command.", color=0xFF0000, timestamp=datetime.datetime.now().astimezone())
            errormsg.set_image("https://i.ibb.co/HYKLGhp/hikrusip.gif")
            errormsg.add_field(name="📜 **__Error Log__**:", value=f"```py\n{exception}```")
            await event.context.respond(content=random.choice(errormsginsert), embed=errormsg)
            logging.error(event.exception)
            raise(event.exception)
    
def load(bot):
    bot.subscribe(lightbulb.CommandErrorEvent, on_error)
    
def unload(bot):
    bot.unsubscribe(lightbulb.CommandErrorEvent, on_error)