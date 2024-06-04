from pydantic import BaseModel


class WhisperRequest(BaseModel):
    cmd: str = "whisper"
    nick: str
    text: str
