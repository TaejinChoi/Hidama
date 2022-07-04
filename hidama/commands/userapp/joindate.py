import lightbulb

joindate_plugin = lightbulb.Plugin("Joindate", "Tells you the date of when someone joined your server.")

@joindate_plugin.command()
@lightbulb.add_cooldown(1200.0, 1, lightbulb.GuildBucket)
@lightbulb.command("Join Date", "See the date and time of when someone joined this particular server by right clicking on anyone and selecting apps.")
@lightbulb.implements(lightbulb.UserCommand)
async def ctx_joined_date(ctx: lightbulb.UserContext) -> None:
    member = ctx.app.cache.get_member(ctx.guild_id, ctx.options.target.id)
    await ctx.respond(f"**{member.display_name}** joined this server on <t:{member.joined_at.timestamp():.0f}:f> local time.")
    
def load(bot):
    bot.add_plugin(joindate_plugin)
    
def unload(bot):
    bot.remove_plugin(joindate_plugin)