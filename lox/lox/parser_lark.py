from pathlib import Path
import lark
from .token import Token, TokenType
from .ast import Binary, Expr, ExprStmt, Identifier, Literal, Return, Unary, Call
from .ast import Block, If, Print, Stmt, Program, Var, Function

BASE = Path(__file__).parent / "grammar.lark"
SOURCE = BASE.read_text()
GRAMMAR = lark.Lark(SOURCE, parser="lalr", start=["program", "expression"])

type Input = str


@lark.v_args(inline=True)
class LoxTransformer(lark.Transformer):
    #
    # Terminais
    #
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

    def IDENTIFIER(self, token: lark.Token):
        return Identifier(str(token))

    #
    # Expr
    #
    def binary(self, left: Expr, op: lark.Token, right: Expr):
        return Binary(left, lox_token(op), right)

    def unary(self, op: lark.Token, right: Expr):
        return Unary(lox_token(op), right)

    def call(self, callee: Expr, args=None):
        return Call(callee, args or [])

    @lark.v_args(inline=False)
    def arguments(self, children: list[Expr]):
        return children

    #
    # Stmt
    #
    @lark.v_args(inline=False)
    def program(self, children):
        return Program(children)

    def expr_stmt(self, expr: Expr):
        return ExprStmt(expr)

    def print_stmt(self, expression):
        return Print(expression)

    def var_decl(self, identifier: Identifier, initializer=None):
        if initializer is None:
            initializer = Literal(None)
        return Var(identifier.name, initializer)

    @lark.v_args(inline=False)
    def block(self, children: list[Stmt]):
        return Block(children)

    def if_stmt(self, cond, then, else_=None):
        if else_ is None:
            else_ = Block([])  # lox: else {}
        return If(cond, then, else_)

    def function(self, identifier: Identifier, parameters: list[str], block: Block):
        return Function(identifier.name, parameters, block.body)

    def return_stmt(self, value: Expr | None = None):
        return Return(value)

    @lark.v_args(inline=False)
    def parameters(self, children: list[Identifier]):
        return [identifier.name for identifier in children]


def tokenize(src: str) -> Input:
    return src


def parse_expression(input: Input) -> Expr:
    tree = GRAMMAR.parse(input, start="expression")
    transformer = LoxTransformer()
    ast = transformer.transform(tree)
    return ast

def parse_program(input: Input) -> Stmt:
    tree = GRAMMAR.parse(input, start="program")
    transformer = LoxTransformer()
    ast = transformer.transform(tree)
    # print("-" * 40)
    # if hasattr(ast, "pretty"):
    #     print(ast.pretty())
    # else:
    #     import rich
    #     rich.print(ast)
    # print("-" * 40)
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