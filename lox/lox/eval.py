from typing import Any
from functools import singledispatch

from .token import TokenType
from .expr import Expr, Value, Literal, Grouping, Unary, Binary, Identifier


@singledispatch
def eval(expr: Expr, ctx: Any) -> Value:
    raise TypeError(f"tipo não suportado: {type(expr)}")

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


def truthy(obj) -> bool:
    if obj is False or obj is None:
        return False
    return True