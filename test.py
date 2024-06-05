from hvicorn import Bot, CommandContext, threaded
from hvicorn.models.server import ChatPackage
from logging import basicConfig, DEBUG
import time, random
import _thread
import traceback
import rich

basicConfig(level=DEBUG)

my_bot = Bot("test_hvicorn", "lounge")
owner_trip = "2ZQ3+0"

@my_bot.startup
@threaded
def greetings(bot: Bot):
    bot.send_message(
        "Hello world! I am hvicorn demo bot.\nCommands:\n\t`.hv editmsg` - demos updatemessage.\n\t`.hv invite` - demos inviting.\n\t`.hv emote` - demos emote.\n\t`.hv threading` - demos multithreading.\nSpecial command: try sending awa"
    )


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
    msg = ctx.bot.send_message("Do you like playing ", editable=True)
    time.sleep(5)
    msg.append(
        random.choice(["Genshin impact", "Honkai impact", "Minecraft", "Project sekai"])
        + "?"
    )


@my_bot.command(".hv invite")
def invite(ctx: CommandContext):
    ctx.bot.invite(ctx.sender.nick, "somechannel")


@my_bot.command(".hv emote")
def emote(ctx: CommandContext):
    ctx.bot.emote("awa")


@my_bot.command(".hv threading")
@threaded
def threading(ctx: CommandContext):
    ctx.respond("Use any command if u want. this command will block for 10secs.")
    time.sleep(10)
    ctx.respond("I'm back!")

@my_bot.command(".hv exec")
@threaded
def execute(ctx: CommandContext):
    if ctx.sender.trip != owner_trip:
        return ctx.respond("I wouldn't do that...")
    try:
        exec(ctx.text.split(" ",1)[1], globals())
    except:
        traceback.print_exc()
    return ctx.respond("Done! check console!")


my_bot.run()
