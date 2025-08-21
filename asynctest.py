from hvicorn import Bot, CommandContext
from asyncio import run

bot = Bot(nick="HvicornTest", channel="lounge")


@bot.startup
async def startup():
    await bot.send_message("Hi this is a hvicorn demo, but in async")


@bot.command("Ping")
async def pong(ctx: CommandContext):
    await ctx.respond("Pong (in async)!")


run(bot.run())
