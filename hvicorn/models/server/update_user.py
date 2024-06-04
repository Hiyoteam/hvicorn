from pydantic import BaseModel
from typing import Union, Optional, Literal

class UpdateUserPackage(BaseModel):
    channel: Optional[str] = None
    cmd: str
    color: Union[bool, str]
    hash: Optional[str] = None
    isBot: Optional[bool] = None
    level: Optional[int] = None
    nick: Optional[str] = None
    time: Optional[int] = None
    trip: Optional[str] = None
    uType: Optional[Literal['user', 'mod', 'admin']] = None
    userid: Optional[int] = None