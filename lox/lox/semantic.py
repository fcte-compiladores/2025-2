from __future__ import annotations
from functools import singledispatch
from dataclasses import dataclass, field
from typing import Literal as LiteralType

from .ast import Function, Return
from .ast import Expr,  Stmt

@dataclass
class Ctx:
    parent: Ctx | None = None
    function_context: LiteralType["toplevel", "function", "method"] = "toplevel"
    errors: list[Exception] = field(default_factory=list)

    def error(self, msg: str):
        error =  RuntimeError(msg)
        self.errors.append(error)

    def push(self):
        return Ctx(
            self,
            function_context=self.function_context,
            errors=self.errors
        )

def semantic_analysis(obj: Expr | Stmt):
    ctx = Ctx()
    analyse(obj, ctx)

    if ctx.errors:
        errors = "\n".join(map(str, ctx.errors))
        raise RuntimeError("Erros encontrados na análise semântica\n" + errors )


@singledispatch
def analyse(obj: Expr| Stmt | list, ctx: Ctx):
     for obj in vars(obj).values():
         if isinstance(obj, (Expr, Stmt, list)):
             analyse(obj, ctx)

@analyse.register
def _(obj: list, ctx: Ctx):
    for item in obj:
        analyse(item, ctx)

@analyse.register
def _(cmd: Return, ctx: Ctx):
    if cmd.value is not None:
        analyse(cmd.value, ctx)
    if ctx.function_context == "toplevel":
        ctx.error("Return fora de função ou método")


@analyse.register
def _(cmd: Function, ctx: Ctx):
    ctx = ctx.push()
    ctx.function_context = "function"
    analyse(cmd.body, ctx)