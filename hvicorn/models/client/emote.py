from pydantic import BaseModel


class EmoteRequest(BaseModel):
    cmd: str = "emote"
    text: str
