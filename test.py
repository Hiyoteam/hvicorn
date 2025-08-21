from hvicorn import Bot, CommandContext, ChatPackage
from logging import basicConfig, DEBUG
from asyncio import run, sleep
import random
import traceback

basicConfig(level=DEBUG)

bot = Bot("test_hvicorn", "test")
owner_trip = "LMeOEB"


@bot.startup
async def greetings():
    await bot.send_message(
        "Hello world! I am hvicorn demo bot.\nCommands:\n\t`.hv editmsg` - demos updatemessage.\n\t`.hv invite` - demos inviting.\n\t`.hv emote` - demos emote.\n\t`.hv threading` - demos multithreading.\n\t`.hv plugin` - test plugin.\n\t`.hv afk` - a test plugin again, but it can mark you as AfKing.\nSpecial command: try sending awa"
    )


@bot.on(ChatPackage)
async def on_chat(msg: ChatPackage):
    if "awa" in msg.text:
        await bot.send_message(
            f"Hey, @{msg.nick}, I see you awa-ing!\nHere's ur info(By hvicorn): {bot.get_user_by_nick(msg.nick)}"
        )
        await sleep(1)
        await bot.whisper(msg.nick, "Here's a *✨secret✨* message for you!")
        await sleep(1)
        await bot.emote(f"hugs {msg.nick}")


@bot.command(".hv editmsg")
async def editmsg(ctx: CommandContext):
    msg = await ctx.bot.send_message("Do you like playing ", editable=True)
    await sleep(5)
    choice = (
        random.choice(["Genshin impact", "Honkai impact", "Minecraft", "Project sekai"])
        + "?"
    )
    await msg.append(choice)


@bot.command(".hv invite")
async def invite(ctx: CommandContext):
    await ctx.bot.invite(ctx.sender.nick, "somechannel")


@bot.command(".hv emote")
async def emote(ctx: CommandContext):
    await ctx.bot.emote("awa")


@bot.command(".hv async")
async def async_command(ctx: CommandContext):
    await ctx.respond("Use any command if u want. this command will block for 10secs.")
    await sleep(10)
    await ctx.respond("I'm back!")


@bot.command(".hv exec")
async def execute(ctx: CommandContext):
    if ctx.sender.trip != owner_trip:
        return await ctx.respond("I wouldn't do that...")
    try:
        exec(ctx.text.split(" ", 2)[2], globals())
    except:
        traceback.print_exc()
    return await ctx.respond("Done! check console!")

async def run_bot():
    await bot.load_plugin("testplugin", command_name=".hv plugin")
    await bot.load_plugin("example_plugin_afk", command_prefix=".hv afk")
    
    await bot.run()

run(run_bot())