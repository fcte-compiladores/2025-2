from dataclasses import dataclass, field
from .token import Token, TokenType

type Char = str  # A single character string
KEYWORDS = {
    "and": TokenType.AND,
    "class": TokenType.CLASS,
    "else": TokenType.ELSE,
    "false": TokenType.FALSE,
    "for": TokenType.FOR,
    "fun": TokenType.FUN,
    "if": TokenType.IF,
    "nil": TokenType.NIL,
    "or": TokenType.OR,
    "print": TokenType.PRINT,
    "return": TokenType.RETURN,
    "super": TokenType.SUPER,
    "this": TokenType.THIS,
    "true": TokenType.TRUE,
    "var": TokenType.VAR,
    "while": TokenType.WHILE,
}


def tokenize(source: str) -> list[Token]:
    scanner = Scanner(source)
    return scanner.scan_tokens()


@dataclass
class Scanner:
    source: str
    start: int = 0
    current: int = 0
    line: int = 1
    tokens: list[Token] = field(default_factory=list)

    def scan_tokens(self) -> list[Token]:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        # Add EOF token at the end
        eof = Token(TokenType.EOF, "", self.line + 1)
        self.tokens.append(eof)

        return self.tokens

    def scan_token(self) -> None:
        char = self.advance()
        match char:
            case "(":
                self.add_token(TokenType.LEFT_PAREN)
            case ")":
                self.add_token(TokenType.RIGHT_PAREN)
            case "{":
                self.add_token(TokenType.LEFT_BRACE)
            case "}":
                self.add_token(TokenType.RIGHT_BRACE)
            case ",":
                self.add_token(TokenType.COMMA)
            case ".":
                self.add_token(TokenType.DOT)
            case "-":
                self.add_token(TokenType.MINUS)
            case "+":
                self.add_token(TokenType.PLUS)
            case ";":
                self.add_token(TokenType.SEMICOLON)
            case "*":
                self.add_token(TokenType.STAR)
            case "/":
                if self.match("/"):
                    self.comment()
                else:
                    self.add_token(TokenType.SLASH)
            case "!":
                if self.match("="):
                    self.add_token(TokenType.BANG_EQUAL)
                else:
                    self.add_token(TokenType.BANG)
            case "=":
                if self.match("="):
                    self.add_token(TokenType.EQUAL_EQUAL)
                else:
                    self.add_token(TokenType.EQUAL)
            case "<":
                if self.match("="):
                    self.add_token(TokenType.LESS_EQUAL)
                else:
                    self.add_token(TokenType.LESS)
            case ">":
                if self.match("="):
                    self.add_token(TokenType.GREATER_EQUAL)
                else:
                    self.add_token(TokenType.GREATER)
            case "\"":
                self.string()
            case " " | "\r" | "\t":
                pass  # Ignore whitespace
            case "\n":
                self.line += 1
            case _ if char.isdigit() and char.isascii():
                self.number()
            case _ if char.isalpha() and char.isascii() or char == "_":
                self.identifier()
            case _:
                self.add_token(TokenType.INVALID)


    def match(self, expected: Char) -> bool:
        if self.is_at_end() or self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def advance(self) -> Char:
        char = self.source[self.current]
        self.current += 1
        return char

    def add_token(self, type: TokenType) -> None:
        text = self.source[self.start:self.current]
        token = Token(type, text, self.line)
        self.tokens.append(token)

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def comment(self) -> None:
        while self.peek() != "\n" and not self.is_at_end():
            self.advance()

    def peek(self) -> Char:
        if self.is_at_end():
            return "\0"
        return self.source[self.current]

    def identifier(self) -> None:
        while self.peek().isalnum() and self.peek().isascii() or self.peek() == "_":
            self.advance()
        self.add_token(TokenType.IDENTIFIER)

        # Check for reserved words
        token = self.tokens[-1]
        if token.lexeme in KEYWORDS:
            token.type = KEYWORDS[token.lexeme]

        match token.lexeme:
            case "true":
                token.literal = True
            case "false":
                token.literal = False
            case "nil":
                token.literal = None


    def string(self) -> None:
        while self.peek() != "\"" and not self.is_at_end():
            self.advance()
        self.advance()  # Consume closing "

        lexeme = self.source[self.start: self.current]
        literal = lexeme[1:-1]  # Strip quotes
        token = Token(TokenType.STRING, lexeme, self.line, literal)
        self.tokens.append(token)

    def number(self) -> None:
        while self.peek().isdigit() and self.peek().isascii():
            self.advance()
        self.add_token(TokenType.NUMBER)

        # Check for reserved words
        token = self.tokens[-1]
        token.literal = float(token.lexeme)