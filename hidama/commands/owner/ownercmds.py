import random
import lightbulb
import hikari
from lightbulb.utils import pag, nav

ownercmds_plugin = lightbulb.Plugin("OwnerCmds", "Commands only usable by Kep1ove.")
ownercmds_plugin.add_checks(lightbulb.owner_only)

@ownercmds_plugin.command
@lightbulb.command("ownerproof", "Hidama's Certificate of Ownership.")
@lightbulb.implements(lightbulb.PrefixCommand)
async def ownerproof(ctx: lightbulb.Context) -> None:
    await ctx.respond("<@992048365619662860> AKA the person running this command is my owner!\n\nKep1er + love = Kep1ove", user_mentions=True)

#@ownercmds_plugin.command
#@lightbulb.option("plugin", "Name of the plugin")
#@lightbulb.command("reload", "Reload a plugin.")
#@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
#async def reload_plugin(ctx: lightbulb.Context) -> None:
#    plugin = ctx.options.plugin
#    await handle_plugins(ctx, plugin, "reload")
    
@ownercmds_plugin.command
@lightbulb.command("byebyehidama", "Shuts down Hidama", aliases=["sd", "shutdown"])
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def shutdown(ctx: lightbulb.Context) -> None:
    await ctx.respond("Bye bye Kep1ove ♥ - I'm shutting down now.")
    await ctx.bot.close()
    
@ownercmds_plugin.command
@lightbulb.command("crash", "Simulate an error", aliases=["errorsim", "errsim"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def crash(ctx: lightbulb.Context) -> None:
    await ctx.respond("Generating Error Message. . .")
    raise ValueError("This is a crash test.")

@ownercmds_plugin.command
@lightbulb.add_cooldown(3, 10, lightbulb.UserBucket)
@lightbulb.option("choices", "What to choose between.", str)
@lightbulb.command("choose", "makes a choice between any number of SPACE SEPARATED words")
@lightbulb.implements(lightbulb.PrefixCommand)
async def choose(ctx: lightbulb.Context, *choices: str):
    await ctx.respond(random.choice(choices))

# Borrowed from https://github.com/kamfretoz/XJ9/blob/main/meta/debug/tools.py
@ownercmds_plugin.command
@lightbulb.add_cooldown(3600, 3, lightbulb.GlobalBucket)
@lightbulb.option("url", "Link to the new avatar URL.", str, required = False)
@lightbulb.command("setavatar","Set the bot's avatar", aliases=["setav"], auto_defer = True, pass_options = True)
@lightbulb.implements(lightbulb.PrefixCommand)
async def setavatar(ctx: lightbulb.Context, url: str):
    if ctx.attachments:
        url = ctx.attachments[0].url
    elif url is None:
        await ctx.respond("Please specify an avatar url if you did not attach a file")
        return
    try:
        await ctx.bot.rest.edit_my_user(avatar=str(hikari.URL(url)))
    except Exception as e:
        await ctx.respond("Whoops, can't change avatar: {}".format(e))
        return
    await ctx.respond(":eyes:")
    
# Borrowed from https://github.com/kamfretoz/XJ9/blob/main/meta/debug/tools.py
@ownercmds_plugin.command
@lightbulb.add_cooldown(3600, 3, lightbulb.GlobalBucket)
@lightbulb.option("name", "name to change to", str, required = True)
@lightbulb.command("setname","Sets the name", aliases=["botname"], auto_defer = True, pass_options = True)
@lightbulb.implements(lightbulb.PrefixCommand)
async def setbotname(ctx: lightbulb.Context, name: str):
    try:
        await ctx.bot.rest.edit_my_user(username=name)
    except Exception as e:
        await ctx.respond("Unable to change the name: {}".format(e))
        return
    await ctx.respond(f"My name is now... `{name}`")
   
# Borrowed from https://github.com/kamfretoz/XJ9/blob/main/meta/debug/tools.py 
@ownercmds_plugin.command
@lightbulb.option("server","The ID of the server", hikari.Snowflake, required = True)
@lightbulb.option("global", "Whether or not to purge global slash commands from the bot.", bool, required = False, default = False)
@lightbulb.command("clearcmd", "purge all slash commands from specified guild", auto_defer=True, pass_options = True)
@lightbulb.implements(lightbulb.PrefixCommand)
async def purge_cmd(ctx: lightbulb.Context, globals: bool, guild: hikari.Snowflake):
    await ctx.respond("Purging application commands...")
    await ctx.bot.purge_application_commands(guild, global_commands=globals)
    await ctx.edit_last_response("Task Completed Successfully!")
   
# Borrowed from https://github.com/kamfretoz/XJ9/blob/main/meta/debug/tools.py 
@ownercmds_plugin.command
@lightbulb.command("synccmd", "Sync slash commands", auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand)
async def sync_cmd(ctx: lightbulb.Context):
    await ctx.respond("Sync In Progress...")
    await ctx.bot.sync_application_commands()
    await ctx.edit_last_response("Task Completed Successfully!")

# Borrowed from https://github.com/kamfretoz/XJ9/blob/main/meta/debug/tools.py   
@ownercmds_plugin.command
@lightbulb.command("serverlist", "Shows a list of the servers I'm in.", auto_defer = True, aliases=["listservers"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def serverlist(ctx: lightbulb.Context):
    guilds = ctx.bot.cache.get_guilds_view().values()
    lst = pag.EmbedPaginator()
    
    @lst.embed_factory()
    def build_embed(page_index,page_content):
        emb = hikari.Embed(title=f"Serverlist (Page {page_index})", description=page_content)
        emb.set_footer(f"{len(guilds)} Servers in total.")
        return emb
    
    for n, guild in enumerate(guilds, start=1):
        lst.add_line(f"**{n}.** **{guild.name}** ({guild.id})")
            
    navigator = nav.ButtonNavigator(lst.build_pages())
    await navigator.run(ctx)

# Borrowed from https://github.com/kamfretoz/XJ9/blob/main/meta/debug/tools.py   
@ownercmds_plugin.command
@lightbulb.option("id", "The ID of server you want me to leave", hikari.Snowflake, required=False)
@lightbulb.command("leaveserver", "Force me to leave a server", auto_defer = True, pass_options = True)
@lightbulb.implements(lightbulb.PrefixCommand)
async def leaveserver(ctx: lightbulb.Context, id: hikari.Snowflake):
    if id is None:
        guild = ctx.get_guild()
    else:
        guild = ctx.bot.cache.get_guild(id)
    await ctx.respond(f"Leaving **{guild.name}**...")
    await ctx.bot.rest.leave_guild(guild)
    await ctx.event.message.add_reaction("👍")
    
def load(bot):
    bot.add_plugin(ownercmds_plugin)
    
def unload(bot):
    bot.remove_plugin(ownercmds_plugin)