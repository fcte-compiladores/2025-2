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

@dataclass
class Call(Expr):
    callee: Expr
    args: list[Expr]


class Stmt:
    """
    Classe base abstrata de todos comandos Lox
    """

@dataclass
class Program(Stmt):
    body: list[Stmt]


@dataclass
class Print(Stmt):
    right: Expr


@dataclass
class ExprStmt(Stmt):
    expr: Expr


@dataclass
class Var(Stmt):
    name: str
    right: Expr


@dataclass
class Block(Stmt):
    body: list[Stmt]


@dataclass
class If(Stmt):
    cond: Expr
    then_body: Stmt
    else_body: Stmt


@dataclass
class While(Stmt):
    cond: Expr
    body: Stmt


@dataclass
class Function(Stmt):
    name: str
    params: list[str]
    body: list[Stmt]


@dataclass
class Class(Stmt):
    name: str
    superclass: str | None
    body: dict[str, Function]

