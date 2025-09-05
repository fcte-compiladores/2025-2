import sys
from pathlib import Path
from .scanner import tokenize


class Lox:
    def run(self, source: str):
        tokens = tokenize(source)

        # For now, just print the tokens.
        for token in tokens:
            print(token)

def main():
    if len(sys.argv) > 2:
        print("Usage: pylox [script]")
        exit(64)
    elif len(sys.argv) == 2:
        path = Path(sys.argv[1])
        run_file(path)
    else:
        run_prompt()


def run_file(path: Path):
    src = path.read_text(encoding=sys.getdefaultencoding())
    lox = Lox()
    lox.run(src)


def run_prompt():
    lox = Lox()

    while True:
        try:
            line = input("> ")
        except EOFError:
            break
        else:
            lox.run(line)


if __name__ == "__main__":
    main()