from pydantic import BaseModel
from typing import Union, Optional, Literal


class OnlineAddPackage(BaseModel):
    channel: Optional[str] = None
    cmd: Literal["onlineAdd"]
    color: Union[bool, str]
    hash: str
    isBot: bool
    level: int
    nick: str
    time: int
    trip: Optional[str] = None
    uType: Literal["user", "mod", "admin"]
    userid: int
