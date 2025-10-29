from pathlib import Path
import lark
from .token import Token, TokenType
from .expr import Binary, Expr, Literal, Unary
from .stmt import Block, If, Print, Stmt, Program

BASE = Path(__file__).parent / "grammar.lark"
SOURCE = BASE.read_text()
GRAMMAR = lark.Lark(SOURCE, parser="lalr", start=["program", "expression"])

type Input = str


@lark.v_args(inline=True)
class LoxTransformer(lark.Transformer):
    def STRING(self, token: lark.Token):
        return Literal(token[1:-1])

    def NUMBER(self, token: lark.Token):
        return Literal(float(token))

    def LITERAL(self, token: lark.Token):
        if token == "true":
            return Literal(True)
        if token == "false":
            return Literal(False)
        if token == "nil":
            return Literal(None)

    def if_stmt(self, cond, then, else_=None):
        if else_ is None:
            else_ = Block([])  # lox: else {}
        return If(cond, then, else_)

    def binary(self, left: Expr, op: lark.Token, right: Expr):
        return Binary(left, lox_token(op), right)

    def unary(self, op: lark.Token, right: Expr):
        return Unary(lox_token(op), right)

    def print_stmt(self, expression):
        return Print(expression)

    @lark.v_args(inline=False)
    def program(self, children):
        return Program(children)


def tokenize(src: str) -> Input:
    return src

def parse_expression(input: Input) -> Expr:
    tree = GRAMMAR.parse(input, start="expression")
    transformer = LoxTransformer()
    ast = transformer.transform(tree)
    return ast

def parse_program(input: Input) -> Stmt:
    tree = GRAMMAR.parse(input, start="program")
    print(tree.pretty())
    transformer = LoxTransformer()
    print("-" * 40)
    ast = transformer.transform(tree)
    if hasattr(ast, "pretty"):
        print(ast.pretty())
    else:
        import rich
        rich.print(ast)
    # exit("tchau!")
    return ast

TOKEN_TYPES = {
    "!": TokenType.BANG,
    "+": TokenType.PLUS,
    "-": TokenType.MINUS,
    "*": TokenType.STAR,
    "/": TokenType.SLASH,
    ">": TokenType.GREATER,
    "<": TokenType.LESS,
    ">=": TokenType.GREATER_EQUAL,
    "<=": TokenType.LESS_EQUAL,
    "==": TokenType.EQUAL_EQUAL,
    "!=": TokenType.BANG_EQUAL,
}


def lox_token(token: lark.Token) -> Token:
    type = TOKEN_TYPES[token]
    return Token(type, str(token), token.line)