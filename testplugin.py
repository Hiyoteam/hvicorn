import hvicorn


def plugin_init(bot: hvicorn.Bot, command_name: str):
    def hello(ctx: hvicorn.CommandContext):
        ctx.respond("Hello from a hvicorn plugin")

    bot.register_command(command_name, hello)
