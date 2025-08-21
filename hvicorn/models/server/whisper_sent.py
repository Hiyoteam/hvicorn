from pydantic import BaseModel
from typing import Literal

from pydantic.fields import Field


class WhisperSentPackage(BaseModel):
    channel: str
    cmd: Literal["info"]
    userid_from: int = Field(..., alias="from")
    text: str
    content: str  # processed by program
    time: int
    userid_to: int = Field(..., alias="to")
    type: str = "whisper"
