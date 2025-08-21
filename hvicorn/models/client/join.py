from typing import Literal, Optional
from pydantic import BaseModel


class JoinRequest(BaseModel):
    cmd: Literal['join'] = "join"
    nick: str
    channel: str
    password: Optional[str] = None
