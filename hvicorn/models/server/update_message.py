from pydantic import BaseModel
from typing import Literal

class UpdateMessagePackage(BaseModel):
    channel: str
    cmd: str
    customId: str
    level: int
    mode: Literal["overwrite", "prepend", "append", "complete"]
    text: str
    time: int
    userid: int