from pydantic import BaseModel
from typing import Optional


class InviteRequest(BaseModel):
    cmd: str = "invite"
    nick: str
    to: Optional[str]
