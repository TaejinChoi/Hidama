import lightbulb
import hikari

slashtest_plugin = lightbulb.Plugin("Slashtest", "Tests if slash commands are working.")

@slashtest_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.GuildBucket)
@lightbulb.command("test", "Checks to see if Hidama is responding to slash commands.")
@lightbulb.implements(lightbulb.SlashCommand)
async def test(ctx: lightbulb.SlashContext) -> None:
    itsworking = "Hidama is responding to slash commands!"
    emb = hikari.Embed(title="Slash Command Test", description=itsworking)
    await ctx.respond(embed=emb)
    
def load(bot):
    bot.add_plugin(slashtest_plugin)
    
def unload(bot):
    bot.remove_plugin(slashtest_plugin)