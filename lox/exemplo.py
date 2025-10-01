from lox.expr import Add, Mul, Sub, Div, Expr, Literal, Value
from functools import singledispatch


# def eval(expr: Expr) -> Value:
#     match expr:
#         case Literal(value):
#             return value
#         case Add(left, right):
#             return eval(left) + eval(right) # type: ignore
#         case Sub(left, right):
#             return eval(left) - eval(right) # type: ignore
#         case Mul(left, right):
#             return eval(left) * eval(right) # type: ignore
#         case Div(left, right):
#             return eval(left) / eval(right) # type: ignore
#         case _:
#             raise NotImplementedError(f"Expressão desconhecida: {expr}")

@singledispatch
def eval(expr: Expr) -> Value:
    raise NotImplementedError(f"Expressão desconhecida: {expr}")

@eval.register
def _(expr: Literal) -> Value:
    return expr.value

@eval.register
def _(expr: Add) -> Value:
    return eval(expr.left) + eval(expr.right)  # type: ignore

@eval.register
def _(expr: Sub) -> Value:
    return eval(expr.left) - eval(expr.right)  # type: ignore

@eval.register
def _(expr: Mul) -> Value:
    return eval(expr.left) * eval(expr.right)  # type: ignore

@eval.register
def _(expr: Div) -> Value:
    return eval(expr.left) / eval(expr.right)  # type: ignore


# 4 * 10 - 2
ast = Sub(
    Mul(Literal(4), Literal(10)),
    Literal(2),
)

print(ast)
print(eval(ast))  # type: ignore