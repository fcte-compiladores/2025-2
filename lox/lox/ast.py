from dataclasses import dataclass
from typing import TYPE_CHECKING

import abc
from .token import Token

if TYPE_CHECKING:
    from .runtime import LoxFunction, NativeFunction, LoxClass, LoxInstance

type Value = str | float | bool | None | LoxFunction | NativeFunction | LoxClass | LoxInstance


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
    distance_to_definition: int | None = None

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
    distance_to_definition: int | None = None

@dataclass
class Call(Expr):
    callee: Expr
    args: list[Expr]


@dataclass
class This(Expr):
    distance_to_definition: int | None = None


@dataclass
class Super(Expr):
    method: str
    distance_to_definition: int | None = None


@dataclass
class Getattr(Expr):
    left: Expr
    attr: str


@dataclass
class Setattr(Expr):
    left: Expr
    attr: str
    right: Expr


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
class Return(Stmt):
    value: Expr | None


@dataclass
class Class(Stmt):
    name: str
    superclass: str | None
    body: list[Function]

