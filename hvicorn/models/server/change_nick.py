from pydantic import BaseModel
class ChangeNickPackage(BaseModel):
    old_nick: str
    new_nick: str
    text: str
    cmd: str
    channel: str
    time: int