from typing import Literal
from pydantic import BaseModel


class CaptchaPackage(BaseModel):
    channel: str
    cmd: Literal['captcha']
    text: str
    time: int
