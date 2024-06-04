from pydantic import BaseModel
from typing import Optional, Literal

class UpdateMessageRequest(BaseModel):
    customId: str
    mode: Literal["overwrite", "prepend", "append"]
    text: str