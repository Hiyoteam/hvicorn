from typing import Literal
from pydantic import BaseModel
from typing import Optional


class InviteRequest(BaseModel):
    cmd: Literal["invite"] = "invite"
    nick: str
    to: Optional[str]
