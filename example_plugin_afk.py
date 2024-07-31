import hvicorn

afked_users = {}


def plugin_init(
    bot: hvicorn.Bot,
    command_prefix: str = "/afk",
    on_afk: str = "You are marked AfK.",
    afk_tip: str = "{nick} is now AfK.",
    already_afk: str = "You are already AfKed.",
    reason: str = "Reason: {reason}",
    welcome_back: str = "Welcome back.",
):

    def mark_afk(ctx: hvicorn.CommandContext):
        reason = ctx.args if ctx.args else None
        if ctx.sender.nick in afked_users.keys():
            return ctx.respond(already_afk)
        afked_users.update({ctx.sender.nick: reason})
        return ctx.respond(on_afk)

    def back_check(event):
        if "nick" not in dir(event):
            return
        if "text" in dir(event) and event.text.startswith(command_prefix):
            return
        if event.nick in afked_users.keys():
            del afked_users[event.nick]
            return bot.send_message(f"@{event.nick} {welcome_back}")

    def on_chat(event: hvicorn.ChatPackage):
        for user in afked_users.items():
            if f"@{user[0]}" in event.text:
                bot.send_message(
                    f"@{event.nick} {afk_tip.format(nick=user[0])}"
                    + (" " + reason.format(reason=user[1]) if user[1] else "")
                )
                return  # only processes the first

    bot.register_command(command_prefix, mark_afk)
    bot.register_global_function(back_check)
    bot.register_event_function(hvicorn.ChatPackage, on_chat)
