import sys

from .expr import Value
from .scanner import tokenize
from .parser import parse_expression, parse_program
from .eval import eval, exec


def main():
    if len(sys.argv) == 1:
        return repl()
    elif len(sys.argv) == 2:
        return run_file(sys.argv[1])
    else:
        exit("Uso: pylox [ NOME DO ARQUIVO ]")


def run_file(path: str):
    with open(path) as f:
        source = f.read()

    lox = Lox()
    lox.run_program(source)


def repl():
    lox = Lox()

    while True:
        try:
            cmd = input(">>> ")
        except (EOFError, KeyboardInterrupt):
            break

        try:
            value = lox.run_expression(cmd)
        except Exception as error:
            typ = type(error).__name__
            print(f"{typ}: {error}")
        else:
            print(value)


class Lox:
    def __init__(self):
        self.ctx = {"x": 10.0, "y": 2.0}

    def run_expression(self, src: str) -> Value:
        tokens = tokenize(src)
        ast = parse_expression(tokens)
        value = eval(ast, self.ctx)
        return value

    def run_program(self, src: str):
        tokens = tokenize(src)
        ast = parse_program(tokens)
        exec(ast, self.ctx)


if __name__ == "__main__":
    main()
