import lightbulb
import hikari

say_plugin = lightbulb.Plugin("Say", "Makes Hidama repeat what you say.")

@say_plugin.command()
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_MESSAGES))
@lightbulb.option("text", "Type the text you'd like Hidama to say.")
@lightbulb.command("say", "Repeats the input text.", aliases=["echo", "repeat"])
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def echo(ctx: lightbulb.Context) -> None:
    await ctx.respond(ctx.options.text)

def load(bot):
    bot.add_plugin(say_plugin)
    
def unload(bot):
    bot.remove_plugin(say_plugin)