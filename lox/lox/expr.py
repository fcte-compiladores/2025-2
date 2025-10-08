from enum import Enum
from dataclasses import dataclass
from .token import TokenType

type Value = str | float | bool | None


class Expr:
    """
    Classe base abstrata de todas as expressões Lox
    """


@dataclass
class Literal(Expr):
    value: Value

@dataclass
class Identifier(Expr):
    name: str

@dataclass
class BinaryOp(Expr):
    left: Expr
    op: TokenType
    right: Expr

