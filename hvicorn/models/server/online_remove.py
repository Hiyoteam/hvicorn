from pydantic import BaseModel


class OnlineRemovePackage(BaseModel):
    nick: str
    cmd: str
    time: int
    userid: int
