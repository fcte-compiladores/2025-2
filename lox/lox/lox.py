from .expr import Value
from .scanner import tokenize
from .parser import parse
from .eval import eval


def main():
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
        ast = parse(tokens)
        value = eval(ast, self.ctx)
        return value


if __name__ == "__main__":
    main()