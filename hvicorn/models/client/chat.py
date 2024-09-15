from pydantic import BaseModel
from typing import Optional, Literal
from hvicorn.models.client.update_message import UpdateMessageRequest
from asyncio import run


class Message:
    """
    A class representing a message that can be edited.

    Attributes:
        text (str): The content of the message.
        customId (Optional[str]): A unique identifier for the message. If provided, the message is editable.
        editable (bool): Indicates whether the message can be edited.
    """

    def __init__(self, text: str, customId: Optional[str] = None) -> None:
        """
        Initialize a Message instance.

        Args:
            text (str): The content of the message.
            customId (Optional[str], optional): A unique identifier for the message. Defaults to None.
        """
        self.text = text
        self.customId = customId
        self.editable = customId != None

    def _generate_edit_request(
        self, mode: Literal["overwrite", "prepend", "append", "complete"], text: str
    ):
        """
        Generate an edit request for the message.

        Args:
            mode (Literal["overwrite", "prepend", "append", "complete"]): The edit mode.
            text (str): The text to be used in the edit.

        Returns:
            UpdateMessageRequest: An object representing the edit request.

        Raises:
            SyntaxError: If the message isn't editable or if customId is missing.
        """
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
        """
        Edit the message by overwriting its content.

        Args:
            text (str): The new content for the message.

        Returns:
            The result of the _edit method call.
        """
        self.text = text
        return self._edit("overwrite", text)

    def prepend(self, text):
        """
        Prepend text to the beginning of the message.

        Args:
            text (str): The text to prepend.

        Returns:
            The result of the _edit method call.
        """
        self.text = text + self.text
        return self._edit("prepend", text)

    def append(self, text):
        """
        Append text to the end of the message.

        Args:
            text (str): The text to append.

        Returns:
            The result of the _edit method call.
        """
        self.text += text
        return self._edit("append", text)

    def complete(self):
        """
        Mark the message as complete, making it non-editable.

        Returns:
            UpdateMessageRequest: An object representing the completion request.

        Raises:
            SyntaxError: If customId is missing.
        """
        if not self.customId:
            raise SyntaxError("Missing customId")
        self.editable = False
        return UpdateMessageRequest(customId=self.customId, mode="complete")

    def __add__(self, string: str):
        """
        Implement the addition operator to append text to the message.

        Args:
            string (str): The text to append.

        Returns:
            Message: The updated Message instance.
        """
        self.append(string)
        return self

    def __radd__(self, string: str):
        """
        Implement the right addition operator to prepend text to the message.

        Args:
            string (str): The text to prepend.

        Returns:
            Message: The updated Message instance.
        """
        self.prepend(string)
        return self


class AsyncMessage:
    """
    An asynchronous version of the Message class.

    Attributes:
        text (str): The content of the message.
        customId (Optional[str]): A unique identifier for the message. If provided, the message is editable.
        editable (bool): Indicates whether the message can be edited.
    """

    def __init__(self, text: str, customId: Optional[str] = None) -> None:
        """
        Initialize an AsyncMessage instance.

        Args:
            text (str): The content of the message.
            customId (Optional[str], optional): A unique identifier for the message. Defaults to None.
        """
        self.text = text
        self.customId = customId
        self.editable = customId != None

    def _generate_edit_request(
        self, mode: Literal["overwrite", "prepend", "append", "complete"], text: str
    ):
        """
        Generate an edit request for the message.

        Args:
            mode (Literal["overwrite", "prepend", "append", "complete"]): The edit mode.
            text (str): The text to be used in the edit.

        Returns:
            UpdateMessageRequest: An object representing the edit request.

        Raises:
            SyntaxError: If the message isn't editable or if customId is missing.
        """
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
        """
        Asynchronously edit the message by overwriting its content.

        Args:
            text (str): The new content for the message.

        Returns:
            The result of the _edit method call.
        """
        self.text = text
        return await self._edit("overwrite", text)

    async def prepend(self, text):
        """
        Asynchronously prepend text to the beginning of the message.

        Args:
            text (str): The text to prepend.

        Returns:
            The result of the _edit method call.
        """
        self.text = text + self.text
        return await self._edit("prepend", text)

    async def append(self, text):
        """
        Asynchronously append text to the end of the message.

        Args:
            text (str): The text to append.

        Returns:
            The result of the _edit method call.
        """
        self.text += text
        return await self._edit("append", text)

    async def complete(self):
        """
        Asynchronously mark the message as complete, making it non-editable.

        Returns:
            UpdateMessageRequest: An object representing the completion request.

        Raises:
            SyntaxError: If customId is missing.
        """
        self.editable = False
        if not self.customId:
            raise SyntaxError("Missing customId")
        return UpdateMessageRequest(customId=self.customId, mode="complete")

    def __add__(self, string: str):
        """
        Implement the addition operator to append text to the message.

        Args:
            string (str): The text to append.

        Returns:
            AsyncMessage: The updated AsyncMessage instance.
        """
        run(self.append(string))
        return self

    def __radd__(self, string: str):
        """
        Implement the right addition operator to prepend text to the message.

        Args:
            string (str): The text to prepend.

        Returns:
            AsyncMessage: The updated AsyncMessage instance.
        """
        run(self.prepend(string))
        return self


class ChatRequest(BaseModel):
    cmd: str = "chat"
    text: str
    customId: Optional[str] = None
