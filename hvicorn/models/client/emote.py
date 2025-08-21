from typing import Literal
from pydantic import BaseModel


class EmoteRequest(BaseModel):
    cmd: Literal['emote'] = "emote"
    text: str
