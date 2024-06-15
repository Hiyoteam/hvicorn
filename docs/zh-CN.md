# hvicorn
为hack.chat准备的高性能&优雅的机器人框架……

# 为什么是 hvicorn?
通常，在您制作Hack.Chat机器人时，您面对的是一堆不可知的JSON数据。“等等，那个字段叫什么来着？`content`还是`text`?”  
而在 hvicorn ,所有的数据包都被一个个的数据类解码为一个*确定*的结构。如果您的编辑器含有类型提示/自动补全功能，您应该能够感觉到它！
[查看在 VS Code 中的 Hinting](hinting.gif)

# 快速开始
使用pip安装hvicorn.
```sh
$ pip3 install hvicorn
```
接下来，我们将创建一个对"Ping"消息响应"Pong"的机器人。

```python
import hvicorn

bot = hvicorn.Bot(nick="PingPongBot", channel="lounge")

@bot.command("Ping")
def pong(ctx: hvicorn.CommandContext):
    return ctx.respond("Pong!")

bot.run()
```

docs wip