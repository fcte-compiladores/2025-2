from dataclasses import dataclass

from .stmt import Block, Program, Print, ExprStmt, Stmt, Var
from .token import Token, TokenType
from .expr import Expr, Literal, Identifier, Binary, Assign



def parse_expression(tokens: list[Token]) -> Expr:
    parser = Parser(tokens)
    return parser.expr()


def parse_program(tokens: list[Token]) -> Program:
    parser = Parser(tokens)
    return parser.program()


@dataclass
class Parser:
    tokens: list[Token]
    pos: int = 0

    def program(self) -> Program:
        """
        program : stmt* EOF
        """
        body = []
        while not self.match(TokenType.EOF):
            body.append(self.stmt())
        return Program(body)

    def stmt(self) -> Stmt:
        """
        stmt : print
             | expr_stmt
             | var
             | block
        """
        match self.peek().type:
            case TokenType.PRINT:
                return self.print()
            case TokenType.VAR:
                return self.var()
            case TokenType.LEFT_BRACE:
                return self.block()
            case _:
                return self.expr_stmt()

    def print(self) -> Stmt:
        """
        print : "print" expr ";"
        """
        self.expect(TokenType.PRINT)
        expr = self.expr()
        self.expect(TokenType.SEMICOLON)
        return Print(expr)

    def expr_stmt(self) -> Stmt:
        """
        expr_stmt : expr ";"
        """
        expr = self.expr()
        self.expect(TokenType.SEMICOLON)
        return ExprStmt(expr)

    def var(self) -> Stmt:
        """
        var : "var" IDENTIFIER [ "=" expr ] ";"
        """
        self.expect(TokenType.VAR)
        name = self.expect(TokenType.IDENTIFIER).lexeme
        if self.match(TokenType.EQUAL):
            expr = self.expr()
        else:
            expr = Literal(None)
        self.expect(TokenType.SEMICOLON)
        return Var(name, expr)

    def block(self) -> Stmt:
        """
        block: "{" stmt* "}"
        """
        self.expect(TokenType.LEFT_BRACE)

        body = []

        while not self.match(TokenType.RIGHT_BRACE):
            body.append(self.stmt())

        return Block(body)


    def expr(self) -> Expr:
        """
        expr : assign
        """
        return self.assign()

    def assign(self) -> Expr:
        """
        assign : [ IDENTIFIER "=" ]* math
        """
        names = []
        while (
            self.peek().type == TokenType.IDENTIFIER
            and self.peek_next().type == TokenType.EQUAL
        ):
            names.append(self.next().lexeme)
            self.next()

        expr = self.math()
        while names:
            expr = Assign(names.pop(), expr)

        return expr

    def math(self) -> Expr:
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
        # TODO!
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
            case (
                TokenType.NUMBER
                | TokenType.STRING
                | TokenType.TRUE
                | TokenType.FALSE
                | TokenType.NIL
            ):
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

    def peek_next(self) -> Token:
        try:
            return self.tokens[self.pos + 1]
        except IndexError:
            return self.tokens[-1]

    def match(self, type: TokenType) -> bool:
        if self.peek().type == type:
            self.next()
            return True
        return False

    def expect(self, type: TokenType) -> Token:
        if self.peek().type != type:
            raise SyntaxError(self.peek())
        return self.next()
