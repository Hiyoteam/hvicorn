from typing import Optional, Literal, Callable, List, Dict, Any, Union
from pydantic import BaseModel
from websocket import create_connection, WebSocket
from hvicorn.models.client import *
from hvicorn.models.server import *
from json import loads, dumps
from hvicorn.utils.generate_customid import generate_customid
from hvicorn.utils.json_to_object import json_to_object, verifyNick
from hvicorn.models.client import CustomRequest
from hvicorn.bot.optional_features import OptionalFeatures
from time import sleep
from traceback import format_exc
from logging import debug, warn
from threading import Thread
import ssl

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
        args: str,
        event: Union[WhisperPackage, ChatPackage],
    ) -> None:
        self.bot: "Bot" = bot
        self.sender: User = sender
        self.triggered_via: Literal["chat", "whisper"] = triggered_via
        self.text: str = text
        self.args: str = args
        self.event: Union[WhisperPackage, ChatPackage] = event

    def respond(self, text, at_sender=True):
        if self.triggered_via == "chat":
            self.bot.send_message(
                ("@" + self.sender.nick + " " if at_sender else "") + str(text)
            )
        elif self.triggered_via == "whisper":
            self.bot.whisper(self.sender.nick, text)
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
        self.wsopt: Dict = {}
        self.killed: bool = False
        self.users: List[User] = []
        self.commands: Dict[str, Callable] = {}
        self.optional_features: OptionalFeatures = OptionalFeatures()

    def _send_model(self, model: BaseModel) -> None:
        if type(model) == CustomRequest:
            payload = model.rawjson
        else:
            try:
                data = model.model_dump()
            except:
                warn(f"Cannot stringify model, ignoring: {model}")
                return
            payload = {}
            for k, v in data.items():
                if v != None:
                    payload.update({k: v})
        if self.websocket:
            debug(f"Sent payload: {payload}")
            self.websocket.send(dumps(payload))
        else:
            warn(f"Websocket isn't open, ignoring: {model}")

    def get_users_by(
        self,
        by: Literal[
            "nick",
            "hash",
            "trip",
            "color",
            "isBot",
            "level",
            "uType",
            "userid",
            "function",
        ],
        matches: Union[str, Callable],
    ) -> List[User]:
        results = []
        for user in self.users:
            if by != "function":
                if user.__dict__.get(by) == matches:
                    results.append(user)
            else:
                if callable(matches):
                    if matches(user):
                        results.append(user)
                else:
                    raise ValueError(f"Function {matches} is not callable")
        return results

    def get_user_by(
        self,
        by: Literal[
            "nick",
            "hash",
            "trip",
            "color",
            "isBot",
            "level",
            "uType",
            "userid",
            "function",
        ],
        matches: Union[str, Callable],
    ) -> Optional[User]:
        result = self.get_users_by(by, matches)
        return result[0] if result else None

    def get_user_by_nick(self, nick: str) -> Optional[User]:
        return self.get_user_by("nick", nick)

    def _internal_handler(self, event: BaseModel) -> None:
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
            user = self.get_user_by_nick(event.nick)
            if user:
                self.users.remove(user)
        if isinstance(event, ChatPackage):
            for command in self.commands.items():
                if event.text.startswith(command[0]):
                    try:
                        user = self.get_user_by_nick(event.nick)
                        if not user:
                            raise RuntimeError("User not found")
                        command[1](
                            CommandContext(
                                self,
                                user,
                                "chat",
                                event.text,
                                event.text.replace(command[0], "", 1).lstrip(),
                                event,
                            )
                        )
                    except:
                        warn(f"Ignoring exception in command: \n{format_exc()}")
        if isinstance(event, WhisperPackage):
            for command in self.commands.items():
                if event.content.startswith(command[0]):
                    try:
                        user = self.get_user_by_nick(event.nick)
                        if not user:
                            raise RuntimeError("User not found")
                        command[1](
                            CommandContext(
                                self,
                                user,
                                "whisper",
                                event.content,
                                event.content.replace(command[0], "", 1).lstrip(),
                                event,
                            )
                        )
                    except:
                        warn(f"Ignoring exception in command: \n{format_exc()}")
        if isinstance(event, UpdateUserPackage):
            if not event.nick:
                return
            target_user = self.get_user_by_nick(event.nick)
            for k, v in event.model_dump().items():
                if (
                    k in dir(target_user)
                    and v != None
                    and v != target_user.__getattribute__(k)
                ):
                    target_user.__setattr__(k, v)

    def _connect(self) -> None:
        debug(f"Connecting to {WS_ADDRESS}, Websocket options: {self.wsopt}")
        if (
            WS_ADDRESS == "wss://hack.chat/chat-ws"
            and self.optional_features.bypass_gfw_dns_poisoning
        ):
            debug(
                f"Connecting to wss://104.131.138.176/chat-ws instead of wss://hack.chat/chat-ws to bypass GFW DNS poisoning"
            )
            warn(
                f"Enabling bypass_gfw_dns_poisoning can bypass GFW's DNS poisoning, but this can cause man-in-the-middle attacks."
            )
            self.websocket = create_connection(
                "wss://104.131.138.176/chat-ws",
                host="hack.chat",
                sslopt={"cert_reqs": ssl.CERT_NONE},
                **self.wsopt,
            )
        else:
            self.websocket = create_connection(WS_ADDRESS, **self.wsopt)
        debug(f"Connected!")
        while not self.websocket or not self.websocket.connected:
            sleep(1)

    def _run_events(self, event_type: Any, args: list):
        for function in self.event_functions.get(event_type, []):
            try:
                function(*args)
            except:
                warn(f"Ignoring exception in event: \n{format_exc()}")

    def join(self) -> None:
        debug(f"Sending join package")
        self._send_model(
            JoinRequest(nick=self.nick, channel=self.channel, password=self.password)
        )
        sleep(1)
        debug(f"Done!")

    def send_message(self, text, editable=False) -> Message:
        customId = generate_customid() if editable else None
        self._send_model(ChatRequest(text=text, customId=customId))

        msg = Message(text, customId)

        def wrapper(*args, **kwargs):
            self._send_model(msg._generate_edit_request(*args, **kwargs))

        msg.__setattr__("_edit", wrapper)
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
        self.nick = nick

    def invite(self, nick: str, channel: Optional[str] = None) -> None:
        self._send_model(InviteRequest(nick=nick, to=channel))

    def ping(self) -> None:
        self._send_model(PingRequest())

    def on(
        self, event_type: Optional[Any] = None
    ) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def wrapper(func: Callable[..., Any]) -> Callable[..., Any]:
            nonlocal event_type
            if event_type is None:
                event_type = "__GLOBAL__"
            if event_type in self.event_functions.keys():
                self.event_functions[event_type].append(func)
                debug(f"Added handler for {event_type}: {func}")
            else:
                self.event_functions[event_type] = [func]
                debug(f"Set handler for {event_type} to {func}")
            return func
        return wrapper

    def startup(self, function: Callable) -> None:
        self.startup_functions.append(function)
        debug(f"Added startup function: {function}")
        return None

    def command(
        self, prefix: str
    ) -> Callable[[Callable[[CommandContext], Any]], Callable[[CommandContext], Any]]:
        def wrapper(func: Callable[[CommandContext], Any]):
            if prefix in self.commands.keys():
                warn(
                    f"Overriding function {self.commands[prefix]} for command prefix {prefix}"
                )
            self.commands[prefix] = func
            return func

        return wrapper

    def register_event_function(self, event_type: Any, function: Callable):
        if event_type in self.event_functions.keys():
            self.event_functions[event_type].append(function)
            debug(f"Added handler for {event_type}: {function}")
        else:
            self.event_functions[event_type] = [function]
            debug(f"Set handler for {event_type} to {function}")

    def register_global_function(self, function: Callable):
        self.register_event_function("__GLOBAL__", function)

    def register_startup_function(self, function: Callable):
        self.startup_functions.append(function)
        debug(f"Added startup function: {function}")

    def register_command(self, prefix: str, function: Callable):
        if prefix in self.commands.keys():
            warn(
                f"Overriding function {self.commands[prefix]} for command prefix {prefix}"
            )
        self.commands[prefix] = function

    def kill(self) -> None:
        self.killed = True
        debug("Killing ws")
        if not self.websocket:
            raise ConnectionError("Websocket is already closed / not open")
        self.websocket.close()

    def close_ws(self) -> None:
        debug("Closing ws")
        if not self.websocket:
            raise ConnectionError("Websocket is already closed / not open")
        self.websocket.close()

    def load_plugin(
        self,
        plugin_name: str,
        init_function: Optional[Callable] = None,
        *args,
        **kwargs,
    ) -> None:
        if not init_function:
            try:
                plugin = __import__(plugin_name)
            except ImportError:
                debug(f"Failed to load plugin {plugin_name}, ignoring")
                return
            if "plugin_init" not in dir(plugin):
                debug(f"Failed to find init function of plugin {plugin_name}, ignoring")
                return
            if not callable(plugin.plugin_init):
                debug(f"Init function of plugin {plugin_name} isn't callable, ignoring")
                return
            try:
                plugin.plugin_init(self, *args, **kwargs)
            except:
                debug(f"Failed to init plugin {plugin_name}: \n{format_exc()}")
                return
        else:
            try:
                init_function(self, *args, **kwargs)
            except:
                debug(f"Failed to init plugin {plugin_name}: \n{format_exc()}")

        debug(f"Loaded plugin {plugin_name}")

    def run(self, ignore_self: bool = True, wsopt: Dict = {}) -> None:
        self.wsopt = wsopt if wsopt != {} else self.wsopt
        self._connect()
        self.join()
        for function in self.startup_functions:
            debug(f"Running startup function: {function}")
            function()
        while not self.killed and self.websocket is not None:
            try:
                package = self.websocket.recv()
            except Exception as e:
                raise RuntimeError("Websocket connection error: ", e)
            if not package:
                debug("Killed")
                self.killed = True
                break
            package_dict: Dict[Any, Any] = loads(package)
            try:
                event = json_to_object(package_dict)
            except Exception as e:
                debug(e)
                warn(
                    f"Failed to parse event, ignoring: {package_dict} cause exception: \n{format_exc()}"
                )
                continue
            debug(f"Got event {type(event)}::{str(event)}")
            if isinstance(
                event,
                (
                    ChatPackage,
                    EmotePackage,
                    OnlineAddPackage,
                    OnlineRemovePackage,
                    WhisperPackage,
                ),
            ):
                if event.nick == self.nick and ignore_self:
                    debug("Found self.nick, ignoring")
                    continue
            else:
                debug("No nick provided in event, passing loopcheck")
            self._run_events("__GLOBAL__", [event])
            self._run_events(type(event), [event])
