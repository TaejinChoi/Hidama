import lightbulb

wordcount_plugin = lightbulb.Plugin("Wordcount", "View word count for the message")

@wordcount_plugin.command()
@lightbulb.command("Word Count", "View the word count for this message.")
@lightbulb.implements(lightbulb.MessageCommand)
async def ctx_word_count(ctx: lightbulb.MessageContext) -> None:
    message = ctx.options.target
    words = len(message.content.split(" "))
    await ctx.respond(f"Message: {message.content}\nWord count: {words:,}")
    
def load(bot):
    bot.add_plugin(wordcount_plugin)
    
def unload(bot):
    bot.remove_plugin(wordcount_plugin)