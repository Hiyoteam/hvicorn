import hvicorn


async def plugin_init(bot: hvicorn.Bot, command_name: str):
    async def hello(ctx: hvicorn.CommandContext):
        await ctx.respond("Hello from a hvicorn plugin")

    bot.register_command(command_name, hello)
