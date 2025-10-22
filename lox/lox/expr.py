from dataclasses import dataclass
from .token import Token

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