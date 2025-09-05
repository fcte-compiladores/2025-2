from dataclasses import dataclass, field

from .token import Token, TokenType 

type Char = str


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
            case "/":
                if self.match("/"):
                    self.comment()
                else:
                    self.add_token(TokenType.SLASH)
            case "\n":
                self.line += 1
            case " " | "\r" | "\t":
                pass
            case _:
                raise SyntaxError(f"Unexpected character: {char} at line {self.line}")

    def advance(self) -> Char:
        char = self.source[self.current]
        self.current += 1
        return char
    
    def peek(self) -> Char:
        if self.is_at_end():
            return "\0"
        return self.source[self.current]
    
    def match(self, expected: Char) -> bool:
        if self.peek() != expected:
            return False
        self.current += 1
        return True
            
    def is_at_end(self) -> bool:
        return self.current >= len(self.source)
    
    def add_token(self, type: TokenType, literal: float | bool | str | None = None) -> None:
        text = self.source[self.start:self.current]
        token = Token(type, text, self.line, literal)
        self.tokens.append(token)

    def comment(self) -> None:
        while self.peek() != "\n" and not self.is_at_end():
            self.advance()