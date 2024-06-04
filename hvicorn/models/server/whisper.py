from pydantic import BaseModel
from typing import Optional, Literal


class WhisperPackage(BaseModel):
    channel: str
    cmd: str
    nick: str  # didn't use from because it's reserved py keyword
    level: int
    text: str
    content: str  # process it in the program!!!
    time: int
    userid_to: int
    trip: Optional[str] = None
    type: Literal["whisper"]
    uType: Literal["user", "mod", "admin"]
