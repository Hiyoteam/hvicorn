from abc import ABC,abstractmethod,abstractproperty,abstractstaticmethod
from typing import Literal, Union, Any

class ABSMiddleWare(ABC):
    properties: dict
    required_arguments: set[str]
    @abstractmethod
    def __init__(self, **kwargs) -> None:
        pass
    @abstractmethod
    def is_connected(self) -> Literal[True,False]:
        pass
    @abstractmethod
    def event_handle(self) -> tuple[str,Any]:
        pass
    @abstractmethod
    def do_action(self, action: str, data: Any) -> Any:
        pass
    @abstractmethod
    def fallback(self, action: str) -> Union[bool, str]:
        pass
    def get_propertie(self, propertie_name: str):
        return self.properties.get(propertie_name)
