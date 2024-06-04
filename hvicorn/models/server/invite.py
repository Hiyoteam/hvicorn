from pydantic import BaseModel
from typing import Literal

class InvitePackage(BaseModel):
    channel: str
    cmd: str
    from_nick: str #do it in program
    inviteChannel: str
    text: str
    time: int
    to_userid: int
    type: Literal["invite"]