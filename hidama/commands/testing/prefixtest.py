import lightbulb
import hikari

prefixtest_plugin = lightbulb.Plugin("PrefixTest", "Tests if prefix commands are working.")

@prefixtest_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.GuildBucket)
@lightbulb.command("test", "Checks to see if Hidama is responding to prefix commands.")
@lightbulb.implements(lightbulb.PrefixCommand)
async def test(ctx: lightbulb.Context) -> None:
    itsworking = "Hidama is responding to prefix commands!"
    emb = hikari.Embed(title="Prefix Command Test", description=itsworking)
    await ctx.respond(embed=emb)
    
def load(bot):
    bot.add_plugin(prefixtest_plugin)
    
def unload(bot):
    bot.remove_plugin(prefixtest_plugin)