from typing import Any
from functools import singledispatch

from .stmt import Block, ExprStmt, Print, Program, Stmt, Var
from .token import TokenType
from .expr import Expr, Value, Literal, Grouping, Unary, Binary, Identifier, Assign


@singledispatch
def eval(expr: Expr, ctx: Any) -> Value:
    raise TypeError(f"[eval] tipo não suportado: {type(expr)}")


@singledispatch
def exec(expr: Stmt, ctx: Any) -> Value:
    raise TypeError(f"[exec] tipo não suportado: {type(expr)}")


@eval.register
def _(expr: Literal, ctx):
    return expr.value


@eval.register
def _(expr: Grouping, ctx):
    return eval(expr.expression, ctx)


@eval.register
def _(expr: Unary, ctx):
    right = eval(expr.right, ctx)
    match expr.operator.type:
        case TokenType.MINUS:
            if isinstance(right, float):
                return -right
            raise RuntimeError(f"operação inválida: -{right}")
        case TokenType.BANG:
            return not truthy(right)
        case token:
            raise RuntimeError(f"operação unária inválida {token}")


@eval.register
def _(expr: Binary, ctx):
    left = eval(expr.left, ctx)
    right = eval(expr.right, ctx)

    match expr.operator.type:
        # Operações matemáticas
        case TokenType.PLUS:
            if isinstance(left, float) and isinstance(right, float):
                return left + right
            elif isinstance(left, str) and isinstance(right, str):
                return left + right
            raise RuntimeError(f"operação inválida: {left} + {right}")
        case TokenType.MINUS:
            if isinstance(left, float) and isinstance(right, float):
                return left - right
            raise RuntimeError(f"operação inválida: {left} - {right}")
        case TokenType.STAR:
            if isinstance(left, float) and isinstance(right, float):
                return left * right
            raise RuntimeError(f"operação inválida: {left} * {right}")

        # ...

        # Comparações
        case TokenType.EQUAL_EQUAL:
            if type(left) != type(right):  # noqa
                return False
            return left == right
        case TokenType.GREATER_EQUAL:
            if isinstance(left, float) and isinstance(right, float):
                return left >= right
            raise RuntimeError(f"operação inválida: {left} >= {right}")
        case TokenType.GREATER:
            if isinstance(left, float) and isinstance(right, float):
                return left > right
            raise RuntimeError(f"operação inválida: {left} > {right}")
        # ...

        case token:
            raise RuntimeError(f"operação binaria inválida {token}")


@eval.register
def _(expr: Identifier, ctx):
    try:
        return ctx[expr.name]
    except KeyError:
        raise RuntimeError(f"variável não existe: {expr.name}")


@eval.register
def _(cmd: Assign, ctx) -> Value:
    value = eval(cmd.right, ctx)
    ctx[cmd.name] = value
    return value


#
# Implementações de exec
#
@exec.register
def _(cmd: Program, ctx):
    for stmt in cmd.body:
        exec(stmt, ctx)

@exec.register
def _(cmd: Print, ctx):
    print(eval(cmd.right, ctx))


@exec.register
def _(cmd: ExprStmt, ctx):
    eval(cmd.expr, ctx)


@exec.register
def _(cmd: Var, ctx):
    value = eval(cmd.right, ctx)
    ctx[cmd.name] = value

@exec.register
def _(cmd: Block, ctx):
    for stmt in cmd.body:
        exec(stmt, ctx)

def truthy(obj) -> bool:
    if obj is False or obj is None:
        return False
    return True
