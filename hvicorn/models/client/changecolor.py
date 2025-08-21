from typing import Literal
from pydantic import BaseModel


class ChangeColorRequest(BaseModel):
    cmd: Literal["changecolor"] = "changecolor"
    color: str = "reset"
