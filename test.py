from hvicorn import Bot, CommandContext, threaded, ChatPackage
from logging import basicConfig, DEBUG
import time, random
import traceback

basicConfig(level=DEBUG)

bot = Bot("test_hvicorn", "lounge")
owner_trip = "2ZQ3+0"


@bot.startup
@threaded
def greetings():
    bot.send_message(
        "Hello world! I am hvicorn demo bot.\nCommands:\n\t`.hv editmsg` - demos updatemessage.\n\t`.hv invite` - demos inviting.\n\t`.hv emote` - demos emote.\n\t`.hv threading` - demos multithreading.\n\t`.hv plugin` - test plugin.\n\t`.hv afk` - a test plugin again, but it can mark you as AfKing.\nSpecial command: try sending awa"
    )


@bot.on(ChatPackage)
def on_chat(msg: ChatPackage):
    if "awa" in msg.text:
        bot.send_message(
            f"Hey, @{msg.nick}, I see you awa-ing!\nHere's ur info(By hvicorn): {bot.get_user_by_nick(msg.nick)}"
        )
        time.sleep(1)
        bot.whisper(msg.nick, "Here's a *✨secret✨* message for you!")
        time.sleep(1)
        bot.emote(f"hugs {msg.nick}")


@bot.command(".hv editmsg")
@threaded
def editmsg(ctx: CommandContext):
    msg = ctx.bot.send_message("Do you like playing ", editable=True)
    time.sleep(5)
    msg.append(
        random.choice(["Genshin impact", "Honkai impact", "Minecraft", "Project sekai"])
        + "?"
    )


@bot.command(".hv invite")
def invite(ctx: CommandContext):
    ctx.bot.invite(ctx.sender.nick, "somechannel")


@bot.command(".hv emote")
def emote(ctx: CommandContext):
    ctx.bot.emote("awa")


@bot.command(".hv threading")
@threaded
def threading(ctx: CommandContext):
    ctx.respond("Use any command if u want. this command will block for 10secs.")
    time.sleep(10)
    ctx.respond("I'm back!")


@bot.command(".hv exec")
@threaded
def execute(ctx: CommandContext):
    if ctx.sender.trip != owner_trip:
        return ctx.respond("I wouldn't do that...")
    try:
        exec(ctx.text.split(" ", 2)[2], globals())
    except:
        traceback.print_exc()
    return ctx.respond("Done! check console!")


bot.load_plugin("testplugin", command_name=".hv plugin")
bot.load_plugin("example_plugin_afk", command_prefix=".hv afk")

bot.run(wsopt={"http_proxy_host": "127.0.0.1", "http_proxy_port": 1087}) # delete wsopt if you don't have to use a proxy
