import lightbulb

oscheck_plugin = lightbulb.Plugin("Oscheck", "Checks whether you're in the official server.")

@oscheck_plugin.command()
@lightbulb.add_cooldown(15.0, 1, lightbulb.GlobalBucket)
@lightbulb.command("oscheck", "Checks whether the server you're in is the official server")
@lightbulb.implements(lightbulb.SlashCommand)
async def oscheck(ctx: lightbulb.SlashContext) -> None:
    await ctx.respond("This command only appears in the official server, Kpop Unlimited.")

def load(bot):
    bot.add_plugin(oscheck_plugin)
    
def unload(bot):
    bot.remove_plugin(oscheck_plugin)