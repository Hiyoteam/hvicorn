from pydantic import BaseModel


class WhisperSentPackage(BaseModel):
    channel: str
    cmd: str
    userid_from: int
    text: str
    content: str  # processed by program
    time: int
    userid_to: int
    type: str = "whisper"
