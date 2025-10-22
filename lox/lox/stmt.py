from dataclasses import dataclass
from .expr import Expr

type Value = str | float | bool | None


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
    body:list[Stmt]