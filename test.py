from hvicorn import Bot
from hvicorn.models.server import ChatPackage
from logging import basicConfig, DEBUG
import time

basicConfig(level=DEBUG)

my_bot = Bot("test_hvicorn", "lounge")


@my_bot.startup
def greetings(bot: Bot):
    message = bot.send_message("Hello world!", editable=True)
    time.sleep(5)
    message.append("And everyone!")


@my_bot.on(ChatPackage)
def on_chat(bot: Bot, msg: ChatPackage):
    if "awa" in msg.text:
        bot.send_message(
            f"Hey, @{msg.nick}, I see you awa-ing!\nHere's ur info(By hvicorn): {my_bot.get_user_by_nick(msg.nick)}"
        )


my_bot.run()
