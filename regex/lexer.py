# OBS.: exemplo inspirado no exemplo do analisador léxico da
# documentação oficial do módulo re no Python.
import re
from dataclasses import dataclass
from typing import Iterator

LEXER_RULES = {
    "NUMBER": r"\d+(\.\d+)?",
    "IDENTIFIER": r"\w+",
    "STRING": r'"[^"]+"',
    "LPAR": r"\(",
    "RPAR": r"\)",
    "LBRACE": r"\{",
    "RBRACE": r"\}",
    "COLON": r";",
    "MUL": r"\*",
    "MINUS": r"-",
    "NOT_EQ": r"!=",
    "NOT": r"!",
    "EQUAL": r"==",
    "SPACE": r"\s",
    "ERROR": r".",
}
GROUPS = [f"(?P<{name}>{pattern})" for name, pattern in LEXER_RULES.items()]
REGEX = re.compile("|".join(GROUPS))
KEYWORDS = { "print", "fun", "if", "for", "else", "while"} # ...

@dataclass
class Token:
    kind: str
    lexeme: str
    lineno: int
    colno: int


def lex(src: str) -> Iterator[Token]:
    lineno = 1
    line_start = 0

    for m in REGEX.finditer(src):
        start, end = m.span()
        lexeme = src[start:end]
        kind = m.lastgroup or "ERROR"

        if kind == "IDENTIFIER" and lexeme in KEYWORDS:
            kind = lexeme.upper()
        if kind == "SPACE":
            if lexeme == "\n":
                lineno += 1
                line_start = m.start() + 1
            continue

        colno = m.start() - line_start + 1
        yield Token(kind, lexeme, lineno, colno)

        # TODO: para casa, tratar o indice da coluna no caso de
        # strings com varias linhas.
        if kind == "STRING":
            lineno += lexeme.count("\n")


if __name__ == "__main__":
    lines: list[str] = []

    while True:
        try:
            line = input("> ")
        except (SystemExit, EOFError):
            break

        if line == "":
            src = "\n".join(lines)
            for token in lex(src):
                print(token)
            lines.clear()
        else:
            lines.append(line)
