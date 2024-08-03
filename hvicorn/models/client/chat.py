from pydantic import BaseModel
from typing import Optional, Literal
from hvicorn.models.client.update_message import UpdateMessageRequest


class Message:
    def __init__(self, text: str, customId: Optional[str] = None) -> None:
        self.text = text
        self.customId = customId
        self.editable = customId != None

    def _generate_edit_request(
        self, mode: Literal["overwrite", "prepend", "append", "complete"], text: str
    ):
        if not self.editable:
            raise SyntaxError("This message isn't editable.")
        if self.customId:
            return UpdateMessageRequest(customId=self.customId, mode=mode, text=text)
        else:
            raise SyntaxError("Missing customId")

    def _edit(
        self, mode: Literal["overwrite", "prepend", "append", "complete"], text: str
    ) -> None: ...

    def edit(self, text):
        self.text = text
        return self._edit("overwrite", text)

    def prepend(self, text):
        self.text = text + self.text
        return self._edit("prepend", text)

    def append(self, text):
        self.text += text
        return self._edit("append", text)

    def complete(self):
        self.editable = False
        return UpdateMessageRequest(customId=self.customId, mode="complete")

    def __add__(self, string: str):
        self.append(string)
        return self.text

    def __radd__(self, string: str):
        self.prepend(string)
        return self.text

class AsyncMessage:
    def __init__(self, text: str, customId: Optional[str] = None) -> None:
        self.text = text
        self.customId = customId
        self.editable = customId != None

    def _generate_edit_request(
        self, mode: Literal["overwrite", "prepend", "append", "complete"], text: str
    ):
        if not self.editable:
            raise SyntaxError("This message isn't editable.")
        if self.customId:
            return UpdateMessageRequest(customId=self.customId, mode=mode, text=text)
        else:
            raise SyntaxError("Missing customId")

    async def _edit(
        self, mode: Literal["overwrite", "prepend", "append", "complete"], text: str
    ) -> None: ...

    async def edit(self, text):
        self.text = text
        return await self._edit("overwrite", text)

    async def prepend(self, text):
        self.text = text + self.text
        return await self._edit("prepend", text)

    async def append(self, text):
        self.text += text
        return await self._edit("append", text)

    async def complete(self):
        self.editable = False
        return UpdateMessageRequest(customId=self.customId, mode="complete")

    def __add__(self, string: str):
        self.append(string)
        return self.text

    def __radd__(self, string: str):
        self.prepend(string)
        return self.text


class ChatRequest(BaseModel):
    cmd: str = "chat"
    text: str
    customId: Optional[str] = None
