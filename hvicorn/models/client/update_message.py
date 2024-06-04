from pydantic import BaseModel
from typing import Optional, Literal


class UpdateMessageRequest(BaseModel):
    cmd: str = "updateMessage"
    customId: str
    mode: Literal["overwrite", "prepend", "append", "complete"]
    text: Optional[str] = None
