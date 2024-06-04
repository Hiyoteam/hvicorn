from pydantic import BaseModel


class WarnPackage(BaseModel):
    text: str
