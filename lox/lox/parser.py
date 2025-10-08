from dataclasses import dataclass

from .token import Token, TokenType
from .expr import Expr, Literal, Identifier, Binary, Unary, Grouping


def parse(tokens: list[Token]) -> Expr:
    parser = Parser(tokens)
    expr = parser.expr()
    return expr


@dataclass
class Parser:
    tokens: list[Token]
    pos: int = 0

    def expr(self) -> Expr:
        """
        expr : term (("+" | "-") term)*
        """
        left = self.term()
        while self.peek().type in (TokenType.PLUS, TokenType.MINUS):
            op = self.next()
            right = self.term()
            left = Binary(left, op, right)
        return left

    def term(self) -> Expr:
        """
        term : pow (("*" | "/") pow)*
        """
        left = self.pow()
        while self.peek().type in (TokenType.STAR, TokenType.SLASH):
            op = self.next()
            right = self.pow()
            left = Binary(left, op, right)
        return left

    def pow(self) -> Expr:
        """
        term : (atom "^")* atom
        """
        return self.atom()

    def atom(self) -> Expr:
        """
        atom : NUMBER
             | STRING
             | BOOL
             | NIL
             | "(" expr ")"
        """
        token = self.next()
        match token.type:
            case TokenType.NUMBER | TokenType.STRING | TokenType.TRUE | TokenType.FALSE | TokenType.NIL:
                return Literal(token.literal)
            case TokenType.IDENTIFIER:
                return Identifier(token.lexeme)
            case TokenType.LEFT_PAREN:
                expr = self.expr()
                if self.next().type != TokenType.RIGHT_PAREN:
                    raise SyntaxError(token)
                return expr
            case _:
                raise SyntaxError(token)

    def next(self) -> Token:
        token = self.tokens[self.pos]
        self.pos += 1
        return token

    def peek(self) -> Token:
        return self.tokens[self.pos]