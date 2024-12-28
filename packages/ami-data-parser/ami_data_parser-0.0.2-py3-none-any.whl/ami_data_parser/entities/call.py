from dataclasses import dataclass
from entities.core import BaseEntitie


@dataclass
class Call(BaseEntitie): 
    channel: str
    position: int
    wait_time: int
    priority: int
    
    def get_key(self) -> str:
        return self.channel
    
    def __eq__(self, value: object) -> bool:

        if type(self) != type(value):
            return False
        
        return bool(
            self.position == value.position and
            self.get_key() == value.get_key()    
        )
    
    def __post_init__(self) -> None:
        self.type = 'call'