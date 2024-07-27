from pydantic import BaseModel

class CustomRequest(BaseModel):
    json: dict