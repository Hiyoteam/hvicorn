from pydantic import BaseModel
class ChangeColorRequest(BaseModel):
    cmd: str = "changecolor"
    color: str = "reset"