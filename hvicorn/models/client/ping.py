from typing import Literal
from pydantic import BaseModel


class PingRequest(BaseModel):
    cmd: Literal["ping"] = "ping"
