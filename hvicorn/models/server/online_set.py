from pydantic import BaseModel
from typing import Optional, Literal, List, Union


class User(BaseModel):
    channel: Optional[str]
    color: Union[str, bool]
    hash: str
    isBot: bool
    isme: bool
    level: int
    nick: str
    trip: Optional[str] = None
    uType: Literal["user", "mod", "admin"]
    userid: int


class OnlineSetPackage(BaseModel):
    cmd: str
    channel: str
    nicks: List[str]
    time: int
    users: List[User]
