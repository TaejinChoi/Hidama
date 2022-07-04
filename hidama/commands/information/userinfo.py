import datetime as dt
import hikari
import lightbulb

userinfo_plugin = lightbulb.Plugin("Userinfo", "Find out some info.")

@userinfo_plugin.command()
@lightbulb.add_cooldown(5, 1, lightbulb.UserBucket)
@lightbulb.option("target", "The member to get information about.", hikari.Member)
@lightbulb.command("userinfo", "Find out some information about a member of the server.")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def userinfo(ctx: lightbulb.Context) -> None:
    target_ = ctx.options.target
    target = (
        target_
        if isinstance(target_, hikari.Member)
        else ctx.get_guild().get_member(target_)
    )
    if not target:
        await ctx.respond("That user is not in the server. You can only look up people who are on the server where the command is run.\n\nWait that didn't sound")
        return

    created_at = int(target.created_at.timestamp())
    joined_at = int(target.joined_at.timestamp())
    roles = (await target.fetch_roles())
        #roles = (await target.fetch_roles())[1:]  # All but @everyone.

    embed = (
        hikari.Embed(
            title="User information",
            description=f"ID: {target.id}",
            colour=hikari.Colour(0x563275),
            timestamp=dt.datetime.now().astimezone(),
        )
        .set_author(name="Information")
        .set_footer(
            text=f"Requested by {ctx.member.display_name}",
            icon=ctx.member.avatar_url,
        )
        .set_thumbnail(target.avatar_url)
        .add_field(name="Discriminator", value=target.discriminator, inline=True)
        .add_field(name="Bot?", value=target.is_bot, inline=True)
        .add_field(name="Number. of roles", value=len(roles), inline=True)
        .add_field(
            name="Created on",
            value=f"<t:{created_at}:d> (<t:{created_at}:R>)",
            inline=False,
        )
        .add_field(
            name="Joined on",
            value=f"<t:{joined_at}:d> (<t:{joined_at}:R>)",
            inline=False,
        )
        .add_field(name="Roles", value=" | ".join(r.mention for r in roles))
    )

    await ctx.respond(embed)


def load(bot):
    bot.add_plugin(userinfo_plugin)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(userinfo_plugin)