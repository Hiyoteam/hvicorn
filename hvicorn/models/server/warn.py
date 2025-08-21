from pydantic import BaseModel
from typing import Literal


class WarnPackage(BaseModel):
    cmd: Literal["warn"]
    text: str
