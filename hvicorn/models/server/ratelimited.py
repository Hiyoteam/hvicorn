from pydantic import BaseModel
from typing import Literal


class RateLimitedPackage(BaseModel):
    type: Literal["CHANNEL_RL", "COLOR_RL", "CHANGENICK_RL", "MESSAGE_RL", "GLOBAL_RL"]
    text: str
