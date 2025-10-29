from dataclasses import dataclass
import abc
from .token import Token

type Value = str | float | bool | None


class Expr(abc.ABC):
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
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

@dataclass
class Unary(Expr):
    operator: Token
    right: Expr

@dataclass
class Grouping(Expr):
    expression: Expr

@dataclass
class Assign(Expr):
    name: str
    right: Expr