from pydantic import BaseModel

class OptionalFeatures(BaseModel):
    bypass_gfw_dns_poisoning: bool = False