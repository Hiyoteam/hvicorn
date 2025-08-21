from pydantic import BaseModel
from typing import Optional, Literal
from pydantic.fields import Field


class WhisperPackage(BaseModel):
    channel: str
    cmd: Literal["info"]
    nick: str = Field(
        ..., alias="from"
    )  # didn't use from because it's reserved py keyword
    text: str
    content: str  # process it in the program!!!
    time: int
    userid_to: int
    trip: Optional[str] = None
    type: Literal["whisper"]
