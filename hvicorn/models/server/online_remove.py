from pydantic import BaseModel

class OnlineRemovePackage(BaseModel):
    channel: str
    nick: str
    cmd: str
    time: int
    userid: int