from ...abstract import ABSMiddleWare
from ...exceptions import MissingArgumentException
from websocket import create_connection
from ssl import CERT_NONE
class HackChatMiddleWare(ABSMiddleWare):
    required_arguments={"nick","channel"}
    def __init__(self, **kwargs) -> None:
        if self.required_arguments <= set(kwargs.keys()):
            raise MissingArgumentException("nick or channel")
