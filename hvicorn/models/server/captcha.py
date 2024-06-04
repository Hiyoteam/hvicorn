from pydantic import BaseModel


class CaptchaPackage(BaseModel):
    channel: str
    cmd: str
    text: str
    time: int
