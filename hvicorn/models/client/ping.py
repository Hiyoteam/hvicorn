from pydantic import BaseModel

class PingRequest(BaseModel):
    cmd: str = "ping"