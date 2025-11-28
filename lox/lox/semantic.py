from __future__ import annotations
from functools import singledispatch
from dataclasses import dataclass, field
from typing import Literal as LiteralType

from .ast import Assign, Block, Function, Identifier, Return, Var
from .ast import Expr, Stmt

type DeclarationType = LiteralType["declared", "defined"]


@dataclass
class Ctx:
    parent: Ctx | None = None
    function_context: LiteralType["toplevel", "function", "method"] = "toplevel"
    errors: list[Exception] = field(default_factory=list)
    declarations: dict[str, DeclarationType] = field(default_factory=dict)

    def error(self, msg: str):
        error = RuntimeError(msg)
        self.errors.append(error)

    def push(self):
        return Ctx(self, function_context=self.function_context, errors=self.errors)

    def declare(self, name: str):
        if name in self.declarations:
            self.error(f"Redeclaracao de variavel: {name}")
        else:
            self.declarations[name] = "declared"

    def define(self, name: str):
        if self.declarations.get(name) != "declared":
            self.error(f"Definindo variável não declarada: {name}")
        else:
            self.declarations[name] = "defined"

    def distance_to_definition(self, name: str) -> int:
        if name in self.declarations:
            return 0
        elif self.parent is None:
            return 0
        else:
            return 1 + self.parent.distance_to_definition(name)


def semantic_analysis(obj: Expr | Stmt):
    ctx = Ctx()
    analyse(obj, ctx)

    if ctx.errors:
        errors = "\n".join(map(str, ctx.errors))
        raise RuntimeError("Erros encontrados na análise semântica\n" + errors)


@singledispatch
def analyse(obj: Expr | Stmt | list, ctx: Ctx):
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
    ctx.declare(cmd.name)
    ctx.define(cmd.name)

    ctx = ctx.push()
    ctx.function_context = "function"
    for argname in cmd.params:
        ctx.declare(argname)
        ctx.define(argname)
    analyse(cmd.body, ctx)


@analyse.register
def _(cmd: Block, ctx: Ctx):
    child_ctx = ctx.push()
    for stmt in cmd.body:
        analyse(stmt, child_ctx)


@analyse.register
def _(cmd: Var, ctx: Ctx):
    ctx.declare(cmd.name)
    analyse(cmd.right, ctx)
    ctx.define(cmd.name)


@analyse.register
def _(cmd: Identifier, ctx: Ctx):
    cmd.distance_to_definition = ctx.distance_to_definition(cmd.name)


@analyse.register
def _(cmd: Assign, ctx: Ctx):
    cmd.distance_to_definition = ctx.distance_to_definition(cmd.name)
    analyse(cmd.right, ctx)
