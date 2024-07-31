from pydantic import BaseModel


class UncatchedPackage(BaseModel):
    rawjson: dict
