from functools import singledispatch

try:
    from rich import print
except ImportError:
    pass

from lox.scanner import tokenize
from lox.parser import parse
from lox.expr import BinaryOp, Expr, Literal, Value
from lox.token import TokenType


@singledispatch
def eval(expr: Expr) -> Value:
    raise NotImplementedError(f"Expressão desconhecida: {expr}")


@eval.register
def _(expr: Literal) -> Value:
    return expr.value


@eval.register
def _(expr: BinaryOp) -> Value:
    match expr.op:
        case TokenType.PLUS:
            return eval(expr.left) + eval(expr.right)  # type: ignore
        case TokenType.MINUS:
            return eval(expr.left) - eval(expr.right)  # type: ignore
        case TokenType.STAR:
            return eval(expr.left) * eval(expr.right)  # type: ignore
        case TokenType.SLASH:
            return eval(expr.left) / eval(expr.right)  # type: ignore
        case _:
            raise TypeError


src = "1 + 2 * 3 / x"

tokens = tokenize(src)
print(tokens)

ast = parse(tokens)
print(ast)

result = eval(ast)
print(result)
