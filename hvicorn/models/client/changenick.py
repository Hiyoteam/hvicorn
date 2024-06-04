from pydantic import BaseModel


class ChangeNickRequest(BaseModel):
    cmd: str = "changenick"
    nick: str
