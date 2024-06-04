from pydantic import BaseModel
from typing import Optional, Literal
from hvicorn.models.client.update_message import UpdateMessageRequest


class Message:
    def __init__(self, text: str, customId: Optional[str] = None) -> None:
        self.text = text
        self.customId = customId
        self.editable = customId != None

    def _edit(
        self, mode: Literal["overwrite", "prepend", "append", "complete"], text: str
    ):
        return UpdateMessageRequest(customId=self.customId, mode=mode, text=text)

    def edit(self, text):
        return self._edit("overwrite", text)

    def prepend(self, text):
        return self._edit("prepend", text)

    def append(self, text):
        return self._edit("append", text)

    def complete(self):
        self.editable = False
        return UpdateMessageRequest(customId=self.customId, mode="complete")


class ChatRequest(BaseModel):
    cmd: str = "chat"
    text: str
    customId: Optional[str] = None
