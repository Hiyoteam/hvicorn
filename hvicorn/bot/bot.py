from typing import Optional, Literal, Callable, List, Dict, Any
from pydantic import BaseModel
from warnings import warn
from websocket import create_connection, WebSocket
from hvicorn.models.client import *
from hvicorn.models.server import *
from json import loads, dumps
from hvicorn.utils.generate_customid import generate_customid
from hvicorn.utils.json_to_object import json_to_object, verifyNick
from time import sleep
from traceback import format_exc
from logging import debug
from threading import Thread

WS_ADDRESS = "wss://hack.chat/chat-ws"


def threaded(func):
    def wrapper(*args, **kwargs):
        Thread(target=func, args=tuple(args), kwargs=kwargs).start()

    return wrapper


class CommandContext:
    def __init__(
        self,
        bot: "Bot",
        sender: User,
        triggered_via: Literal["chat", "whisper"],
        text: str,
    ) -> None:
        self.bot = bot
        self.sender = sender
        self.triggered_via = triggered_via
        self.text = text

    def respond(self, text, at_sender=True):
        if self.triggered_via == "chat":
            self.bot.send_message(
                ("@" + self.sender.nick + " " if at_sender else "") + str(text)
            )
        elif self.triggered_via == "whisper":
            self.bot.whisper(self.triggered_by.nick, text)
        else:
            warn("Unknown trigger method, ignoring")


class Bot:
    def __init__(self, nick: str, channel: str, password: Optional[str] = None) -> None:
        self.nick = nick
        self.channel = channel
        self.password = password
        self.websocket: Optional[WebSocket] = None
        self.startup_functions: List[Callable] = []
        self.event_functions: Dict[Any, List[Callable]] = {
            "__GLOBAL__": [self._internal_handler]
        }
        self.killed: bool = False
        self.users: List[User] = []
        self.commands: Dict[str, Callable] = {}

    def _send_model(self, model: BaseModel) -> None:
        try:
            data = model.model_dump()
        except:
            warn(f"Cannot stringify model, ignoring: {model}")
        payload = {}
        for k, v in data.items():
            if v != None:
                payload.update({k: v})
        if self.websocket:
            debug(f"Sent payload: {payload}")
            self.websocket.send(dumps(payload))
        else:
            warn(f"Websocket isn't open, ignoring: {model}")

    def get_user(
        self,
        by: Literal[
            "nick", "hash", "trip", "color", "isBot", "level", "uType", "userid"
        ],
        matches: str,
    ) -> Optional[User]:
        for user in self.users:
            if user.__dict__.get(by) == matches:
                return user
        return None

    def get_users(
        self,
        by: Literal[
            "nick", "hash", "trip", "color", "isBot", "level", "uType", "userid"
        ],
        matches: str,
    ) -> List[User]:
        results = []
        for user in self.users:
            if user.__dict__.get(by) == matches:
                results.append(user)
        return results

    def get_user_by_nick(self, nick: str) -> Optional[User]:
        return self.get_user("nick", nick)

    def _internal_handler(self, bot: "Bot", event: BaseModel) -> None:
        if isinstance(event, OnlineSetPackage):
            self.users = event.users
        elif isinstance(event, OnlineAddPackage):
            self.users.append(
                User(
                    channel=event.channel,
                    color=event.color,
                    hash=event.hash,
                    isBot=event.isBot,
                    isme=False,
                    level=event.level,
                    nick=event.nick,
                    trip=event.trip,
                    uType=event.uType,
                    userid=event.userid,
                )
            )
        elif isinstance(event, OnlineRemovePackage):
            if self.get_user_by_nick(event.nick):
                self.users.remove(self.get_user_by_nick(event.nick))
        if isinstance(event, ChatPackage):
            for command in self.commands.items():
                if event.text.startswith(command[0]):
                    try:
                        command[1](
                            CommandContext(
                                self,
                                self.get_user_by_nick(event.nick),
                                "chat",
                                event.text,
                            )
                        )
                    except:
                        warn(f"Ignoring exception in command: \n{format_exc()}")
        if isinstance(event, WhisperPackage):
            for command in self.commands.items():
                if event.content.startswith(command[0]):
                    try:
                        command[1](
                            CommandContext(
                                self,
                                self.get_user_by_nick(event.nick),
                                "whisper",
                                event.content,
                            )
                        )
                    except:
                        warn(f"Ignoring exception in command: \n{format_exc()}")

    def _connect(self) -> None:
        self.websocket = create_connection(WS_ADDRESS)
        while not self.websocket.connected:
            sleep(1)

    def _run_events(self, event_type: Any, args: list):
        for function in self.event_functions.get(event_type, []):
            try:
                function(*args)
            except:
                warn(f"Ignoring exception in event: \n{format_exc()}")

    def join(self) -> None:
        self._send_model(
            JoinRequest(nick=self.nick, channel=self.channel, password=self.password)
        )
        sleep(1)

    def send_message(self, text, editable=False) -> Message:
        customId = generate_customid() if editable else None
        self._send_model(ChatRequest(text=text, customId=customId))

        def wrapper(
            mode: Literal["overwrite", "prepend", "append", "complete"], text: str
        ):
            self._send_model(
                UpdateMessageRequest(customId=msg.customId, mode=mode, text=text)
            )

        msg = Message(text, customId)
        msg._edit = wrapper
        return msg

    def whisper(self, nick: str, text: str) -> None:
        self._send_model(WhisperRequest(nick=nick, text=text))

    def emote(self, text: str) -> None:
        self._send_model(EmoteRequest(text=text))

    def change_color(self, color: str = "reset") -> None:
        self._send_model(ChangeColorRequest(color=color))

    def change_nick(self, nick: str) -> None:
        if not verifyNick(nick):
            raise ValueError("Invaild Nickname")
        self._send_model(ChangeNickRequest(nick=nick))

    def invite(self, nick: str, channel: Optional[str] = None) -> None:
        self._send_model(InviteRequest(nick=nick, to=channel))

    def on(self, event_type: Any = None) -> None:
        def wrapper(func: Callable):
            nonlocal event_type
            if event_type is None:
                event_type = "__GLOBAL__"
            if event_type in self.event_functions.keys():
                self.event_functions[event_type].append(func)
                debug(f"Added handler for {event_type}: {func}")
            else:
                self.event_functions[event_type] = [func]
                debug(f"Set handler for {event_type} to {func}")

        return wrapper

    def startup(self, function: Callable) -> None:
        self.startup_functions.append(function)
        debug(f"Added startup function: {function}")
        return None

    def command(self, prefix: str) -> None:
        def wrapper(func: Callable):
            self.commands[prefix] = func

        return wrapper

    def kill(self) -> None:
        self.killed = True
        debug("Killing ws")
        self.websocket.close()

    def run(self, ignore_self: bool = True) -> None:
        self._connect()
        self.join()
        for function in self.startup_functions:
            debug(f"Running startup function: {function}")
            function(self)
        while not self.killed:
            package = self.websocket.recv()
            if not package:
                debug("Killed")
                self.killed = True
                break
            package = loads(package)
            try:
                event = json_to_object(package)
            except Exception as e:
                debug(e)
                warn(
                    f"Failed to parse event, ignoring: {package} cause exception: \n{format_exc()}"
                )
                continue
            debug(f"Got event {type(event)}::{str(event)}")
            try:
                if event.nick == self.nick and ignore_self:
                    debug("Found self.nick, ignoring")
                    continue
            except:
                debug("No nick provided in event, passing loopcheck")
            self._run_events("__GLOBAL__", [self, event])
            self._run_events(type(event), [self, event])
