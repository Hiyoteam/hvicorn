from typing import Literal
from pydantic import BaseModel


class ChangeNickPackage(BaseModel):
    old_nick: str
    new_nick: str
    text: str
    cmd: Literal["changenick"]
    channel: str
    time: int
