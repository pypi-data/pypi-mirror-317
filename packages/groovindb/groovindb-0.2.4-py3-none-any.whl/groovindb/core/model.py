from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class Field:
    type: str
    nullable: bool = False
    default: Optional[Any] = None

class Model:
    __table__: str
    __fields__: Dict[str, Field]

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value) 