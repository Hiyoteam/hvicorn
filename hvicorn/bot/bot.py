from typing import Optional, Literal, Callable, List, Dict, Any
from pydantic import BaseModel
from warnings import warn
from websocket import create_connection, WebSocket
from hvicorn.models.client import (
    JoinRequest,
    ChatRequest,
    Message,
    UpdateMessageRequest,
    WhisperRequest,
)
from hvicorn.models.server import (
    User,
    OnlineSetPackage,
    OnlineAddPackage,
    OnlineRemovePackage,
)
from json import loads, dumps
from hvicorn.utils.generate_customid import generate_customid
from hvicorn.utils.json_to_object import json_to_object
from time import sleep
from traceback import format_exc
from logging import debug

WS_ADDRESS = "wss://hack.chat/chat-ws"


class Bot:
    def __init__(self, nick: str, channel: str, password: Optional[str] = None) -> None:
        self.nick = nick
        self.channel = channel
        self.password = password
        self.websocket: Optional[WebSocket] = None
        self.startup_functions: List[Callable] = []
        self.event_functions: Dict[Any, List[Callable]] = {}
        self.global_functions: List[Callable] = [self._internal_handler]
        self.killed: bool = False
        self.users: List[User] = []

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

    def get_user_by_nick(self, nick: str) -> Optional[User]:
        for user in self.users:
            if user.nick == nick:
                return user
        return None

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

    def _connect(self) -> None:
        self.websocket = create_connection(WS_ADDRESS)
        while not self.websocket.connected:
            sleep(1)

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

    def on(self, event_type: Any = None) -> None:
        def wrapper(func: Callable):
            if event_type is None:
                self.global_functions.append(func)
                debug(f"Added global handler {func}")
            else:
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
            package = loads(self.websocket.recv())
            try:
                event = json_to_object(package)
            except Exception as e:
                warn(
                    f"Failed to parse event, ignoring: {package} cause exception: \n{format_exc()}"
                )
                continue
            debug(f"Get event {str(event)[:10]}..., type: {type(event)}")
            try:
                if event.nick == self.nick and ignore_self:
                    debug("Found self.nick, ignoring")
                    continue
            except:
                pass
            for function in self.global_functions:
                debug(f"Running {function}")
                try:
                    function(self, event)
                except:
                    warn(f"Exception in global handler, ignoring: \n{format_exc()}")
            for function in self.event_functions.get(type(event), []):
                debug(f"Running {function}")
                try:
                    function(self, event)
                except:
                    warn(f"Exception in handler, ignoring: \n{format_exc()}")
