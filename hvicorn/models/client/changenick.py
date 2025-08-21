from typing import Literal
from pydantic import BaseModel


class ChangeNickRequest(BaseModel):
    cmd: Literal["changenick"] = "changenick"
    nick: str
