from pydantic import BaseModel
from typing import Literal


class LockroomPackage(BaseModel):
    cmd: Literal["info"]
    time: int
