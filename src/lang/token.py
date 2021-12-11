from enum import Enum, auto
from dataclasses import dataclass

class TokenType(Enum):
    MetadataTag = auto(),
    MetadataAssignment = auto(),
    StringText = auto(),
    Header = auto()

@dataclass
class Token:
    type: TokenType
    value: str