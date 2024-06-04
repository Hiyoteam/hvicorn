from pydantic import BaseModel
from typing import Optional, Literal

class EmotePackage(BaseModel):
    channel: str
    cmd: Literal["emote"]
    nick: str
    text: str
    content: str # do this in the program.
    time: int
    trip: Optional[str] = None
    userid: int