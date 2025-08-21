from pydantic import BaseModel
from typing import Literal


class OnlineRemovePackage(BaseModel):
    nick: str
    cmd: Literal["onlineRemove"]
    time: int
    userid: int
