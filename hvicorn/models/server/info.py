from pydantic import BaseModel
from typing import Literal


class InfoPackage(BaseModel):
    cmd: Literal["info"]
    text: str
