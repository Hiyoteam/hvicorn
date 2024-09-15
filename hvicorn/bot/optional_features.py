from pydantic import BaseModel


class OptionalFeatures(BaseModel):
    """
    Optional features configuration.
    """

    bypass_gfw_dns_poisoning: bool = False
    """
    Flag to enable bypassing of GFW DNS poisoning.

    Defaults to False.
    """
