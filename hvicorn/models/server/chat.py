from pydantic import BaseModel
from typing import Optional, Literal


class ChatPackage(BaseModel):
    cmd: Literal["chat"]
    channel: str
    color: Optional[str] = None
    level: int
    nick: str
    text: str
    time: int
    trip: Optional[str] = None
    uType: Literal["user", "mod", "admin"]
    userid: int
    customId: Optional[str] = None
