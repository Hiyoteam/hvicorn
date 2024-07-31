from pydantic import BaseModel


class CustomRequest(BaseModel):
    rawjson: dict
