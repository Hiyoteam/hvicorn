from hvicorn import Bot, CommandContext, threaded
from hvicorn.models.server import ChatPackage
from logging import basicConfig, DEBUG
import time, random

basicConfig(level=DEBUG)

my_bot = Bot("test_hvicorn", "lounge")


@my_bot.startup
@threaded
def greetings(bot: Bot):
    bot.send_message("Hello world! I am hvicorn demo bot.\nCommands:\n\t`.hv editmsg` - demos updatemessage.\n\t`.hv invite` - demos inviting.\n\t`.hv emote` - demos emote.\n\tSpecial command: try sending awa")


@my_bot.on(ChatPackage)
def on_chat(bot: Bot, msg: ChatPackage):
    if "awa" in msg.text:
        bot.send_message(
            f"Hey, @{msg.nick}, I see you awa-ing!\nHere's ur info(By hvicorn): {my_bot.get_user_by_nick(msg.nick)}"
        )
        time.sleep(1)
        bot.whisper(msg.nick, "Here's a *✨secret✨* message for you!")
        time.sleep(1)
        bot.emote(f"hugs {msg.nick}")


@my_bot.command(".hv editmsg")
@threaded
def editmsg(ctx: CommandContext):
    msg=ctx.bot.send_message("Do you like playing ", editable=True)
    time.sleep(5)
    msg.append(random.choice(["Genshin impact","Honkai impact","Minecraft","Project sekai"])+"?")

@my_bot.command(".hv invite")
def invite(ctx: CommandContext):
    ctx.bot.invite(ctx.triggered_by.nick, "somechannel")

@my_bot.command(".hv emote")
def emote(ctx: CommandContext):
    ctx.bot.emote("awa")

my_bot.run()
