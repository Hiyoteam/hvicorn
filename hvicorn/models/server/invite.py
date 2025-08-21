from pydantic import BaseModel, Field
from typing import Literal


class InvitePackage(BaseModel):
    channel: str
    cmd: Literal['invite']
    from_nick: str = Field(..., alias="from")
    invite_channel: str = Field(..., alias="inviteChannel")
    text: str
    time: int
    to_userid: int
    type: Literal["invite"]
