from pydantic import BaseModel
from typing import Literal


class WhisperRequest(BaseModel):
    cmd: Literal["whisper"] = "whisper"
    nick: str
    text: str
