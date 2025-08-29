from typing import Callable
from dataclasses import dataclass
import operator
import math

type Value = float | Callable[..., Value]
type AST = list
type IR = list | Value

FUNCTIONS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "%": operator.mod,
    "/": operator.truediv,
    "sqrt": math.sqrt,
    "cos": math.cos,
    "sin": math.sin,
}

@dataclass
class Token:
    text: str
    kind: str
    value: Value = None

def lex(code: str) -> list[Token]:
    """
    Análise léxica do código.
    """
    code = code.replace("(", " ( ").replace(")", " ) ")
    lexemes = code.split()
    tokens = []

    for lexeme in lexemes:
        if lexeme == "(":
            token = Token(lexeme, "LPAREN")
        elif lexeme == ")":
            token = Token(lexeme, "RPAREN")
        elif lexeme in FUNCTIONS:
            function = FUNCTIONS[lexeme]
            token = Token(lexeme, "FUNCTION", function)
        else:
            value = float(lexeme)
            token = Token(lexeme, "NUMBER", value)

        tokens.append(token)

    return tokens


def parse(tokens: list[Token]) -> AST:
    """
    Análise sintática do código.
    """
    ast = None
    stack = []
    for token in tokens:
        if token.kind == "LPAREN":
            ast = []
            stack.append(ast)
        elif token.kind == "RPAREN":
            result = stack.pop()
            if stack == []:
                return result
            stack[-1].append(result)
        else:
            ast.append(token.value)
    raise SyntaxError


def analysis(ast: AST) -> IR:
    """
    Análise semântica do código.
    """
    # Não fazemos nada aqui :)
    ir = ast
    return ir


def interpret(ir: IR) -> Value:
    """
    Interpreta o código
    """
    if isinstance(ir, list):
        func, *args = [interpret(x) for x in ir]
        return func(*args)
    else:
        return ir


def run(source: str):
    token = lex(source)
    ast = parse(token)
    ir = analysis(ast)
    value = interpret(ir)
    print("=> ", value)


def run_shell():
    print("LISP Interpreter")
    while True:
        try:
            source = input("λ ")
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break
        
        try:
            run(source)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    import sys

    if len(sys.argv) == 2:
        filename = sys.argv[1]
        with open(filename) as f:
            code = f.read()
        run(code)
    else:
        run_shell()

   