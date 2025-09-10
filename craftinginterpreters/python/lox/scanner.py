from dataclasses import dataclass, field
from typing import Any

from .tokens import Token
from .tokens import TokenType as TT

KEYWORDS = {
    "and": TT.AND,
    "class": TT.CLASS,
    "else": TT.ELSE,
    "false": TT.FALSE,
    "for": TT.FOR,
    "fun": TT.FUN,
    "if": TT.IF,
    "nil": TT.NIL,
    "or": TT.OR,
    "print": TT.PRINT,
    "return": TT.RETURN,
    "super": TT.SUPER,
    "this": TT.THIS,
    "true": TT.TRUE,
    "var": TT.VAR,
    "while": TT.WHILE,
}


@dataclass
class Scanner:
    source: str
    start: int = 0
    current: int = 0
    line: int = 1
    tokens: list[Token] = field(default_factory=list)

    def scan_tokens(self) -> list[Token]:
        while not self.is_at_end():
            # We are at the beginning of the next lexeme.
            self.start = self.current
            self.scan_token()
        self.tokens.append(Token(TT.EOF, "", self.line))
        return self.tokens

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def scan_token(self):
        match self.advance():
            case "(":
                self.add_token(TT.LEFT_PAREN)
            case ")":
                self.add_token(TT.RIGHT_PAREN)
            case "{":
                self.add_token(TT.LEFT_BRACE)
            case "}":
                self.add_token(TT.RIGHT_BRACE)
            case ",":
                self.add_token(TT.COMMA)
            case ".":
                self.add_token(TT.DOT)
            case "-":
                self.add_token(TT.MINUS)
            case "+":
                self.add_token(TT.PLUS)
            case ";":
                self.add_token(TT.SEMICOLON)
            case "*":
                self.add_token(TT.STAR)
            case "!" if self.match("="):
                self.add_token(TT.BANG_EQUAL)
            case "!":
                self.add_token(TT.BANG)
            case "=" if self.match("="):
                self.add_token(TT.EQUAL_EQUAL)
            case "=":
                self.add_token(TT.EQUAL)
            case "<" if self.match("="):
                self.add_token(TT.LESS_EQUAL)
            case "<":
                self.add_token(TT.LESS)
            case ">" if self.match("="):
                self.add_token(TT.GREATER_EQUAL)
            case ">":
                self.add_token(TT.GREATER)
            case "/" if self.match("/"):
                # A comment goes until the end of the line.
                while self.peek() != "\n" and not self.is_at_end():
                    self.advance()
            case "/":
                self.add_token(TT.SLASH)
            case " " | "\r" | "\t":
                pass  # Ignore whitespace.
            case "\n":
                self.line += 1
            case '"':
                self.string()
            case "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9":
                self.number()
            case c if is_alpha(c):
                self.identifier()

    def advance(self) -> str:
        char = self.source[self.current]
        self.current += 1
        return char

    def add_token(self, type: TT, literal: Any = None):
        text = self.source[self.start : self.current]
        self.tokens.append(Token(type, text, self.line, literal))

    def match(self, expected: str) -> bool:
        if self.is_at_end() or self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def peek(self) -> str:
        if self.is_at_end():
            return ""
        return self.source[self.current]

    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == "\n":
                self.line += 1
            self.advance()

        if self.is_at_end():
            raise LoxError(self.line, "Unterminated string.")

        # The closing ".
        self.advance()

        # Trim the surrounding quotes.
        value = self.source[self.start + 1 : self.current - 1]
        self.add_token(TT.STRING, value)

    def number(self):
        while is_digit(self.peek()):
            self.advance()

        # Look for a fractional part.
        if self.peek() == "." and is_digit(self.peek_next()):
            # Consume the "."
            self.advance()

        while is_digit(self.peek()):
            self.advance()

        substring = self.source[self.start : self.current]
        self.add_token(TT.NUMBER, float(substring))

    def identifier(self):
        while is_alpha_numeric(self.peek()):
            self.advance()
        text = self.source[self.start : self.current]
        kind = KEYWORDS.get(text, TT.IDENTIFIER)
        self.add_token(kind)


def is_digit(char: str) -> bool:
    return char.isdigit() and char.isascii()


def is_alpha(char: str) -> bool:
    return char == "_" or char.isalpha() and char.isascii()


def is_alpha_numeric(char: str) -> bool:
    return is_alpha(char) or is_digit(char)


def tokenize(source: str) -> list[Token]:
    scanner = Scanner(source)
    return scanner.scan_tokens()
