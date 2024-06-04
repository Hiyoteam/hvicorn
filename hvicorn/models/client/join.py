from typing import Optional
from pydantic import BaseModel

class JoinRequest(BaseModel):
    cmd: str = "join"
    nick: str
    channel: str
    password: Optional[str] = None