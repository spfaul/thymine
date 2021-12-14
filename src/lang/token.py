from enum import Enum, auto
from typing import Union
from dataclasses import dataclass

class TokenType(Enum):
    MetadataTag = auto(),
    MetadataAssignment = auto(),
    StringText = auto(),
    Header = auto(),
    QuoteBlock = auto(),
    BulletPoint = auto()


class Token:
    def __init__(self, token_type, value, parent=None, **kwargs):
        self.type: TokenType = token_type
        self.value: str = value
        self.parent: Union[Token, None] = parent

        for key, val in kwargs.items():
            setattr(self, key, val)

    def __repr__(self):
        return f"<Token type={self.type} value={self.value} parent={self.parent} attrs={self.attrs}>"