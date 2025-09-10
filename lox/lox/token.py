from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
    # Single-character tokens.
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    COMMA = auto()
    DOT = auto()
    SEMICOLON = auto()
    MINUS = auto()
    PLUS = auto()
    SLASH = auto(); STAR = auto()

    # One or two character tokens.
    BANG = auto()
    BANG_EQUAL = auto()
    EQUAL= auto()
    EQUAL_EQUAL = auto()
    GREATER= auto()
    GREATER_EQUAL = auto()
    LESS= auto()
    LESS_EQUAL = auto()

    # Literals.
    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()

    # Keywords.
    AND = auto()
    CLASS = auto()
    ELSE = auto()
    FALSE = auto()
    FUN = auto()
    FOR = auto()
    IF = auto()
    NIL = auto()
    OR = auto()
    PRINT = auto()
    RETURN = auto()
    SUPER = auto()
    THIS = auto()
    TRUE = auto()
    VAR = auto()
    WHILE = auto()

    # Special tokens.
    EOF = auto()
    INVALID = auto()
    UNTERMINATED_STRING = auto()


@dataclass
class Token:
    type: TokenType
    lexeme: str
    line: int
    literal: float | str | bool | None = None

    def __str__(self):
        return f"{self.type.name} {self.lexeme!r} {self.literal}"

    def __repr__(self):
        return str(self)
