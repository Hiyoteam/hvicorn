import hvicorn


def plugin_init(bot: hvicorn.Bot, command_name: str):
    @bot.command(command_name)
    def hello(ctx: hvicorn.CommandContext):
        ctx.respond("Hello from a hvicorn plugin")
