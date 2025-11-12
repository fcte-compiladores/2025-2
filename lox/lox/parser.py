from dataclasses import dataclass

from .ast import Expr, Literal, Identifier, Binary, Assign
from .ast import Block, If, Program, Print, ExprStmt, Stmt, Var, While
from .token import Token, TokenType


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
        program : declaration* EOF
        """
        body = []
        while not self.match(TokenType.EOF):
            body.append(self.declaration())
        return Program(body)

    def declaration(self) -> Stmt:
        """
        declaration : var
                    | function
                    | class
                    | stmt
        """
        match self.peek().type:
            case TokenType.VAR:
                return self.var()
            case TokenType.FUN:
                return self.function()
            case TokenType.CLASS:
                return self.class_()
            case _:
                return self.stmt()

    def stmt(self) -> Stmt:
        """
        stmt : print
             | expr_stmt
             | if_stmt
             | while_stmt
             | for_stmt
             | block
        """
        match self.peek().type:
            case TokenType.PRINT:
                return self.print()
            case TokenType.IF:
                return self.if_stmt()
            case TokenType.WHILE:
                return self.while_stmt()
            case TokenType.FOR:
                return self.for_stmt()
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
        block: "{" declaration* "}"
        """
        self.expect(TokenType.LEFT_BRACE)

        body = []

        while not self.match(TokenType.RIGHT_BRACE):
            body.append(self.declaration())

        return Block(body)

    def if_stmt(self) -> If:
        """
        if_stmt : "if" "(" expr ")" stmt [ "else" stmt ]
        """
        self.expect(TokenType.IF)
        self.expect(TokenType.LEFT_PAREN)
        cond = self.expr()
        self.expect(TokenType.RIGHT_PAREN)
        then_body = self.stmt()

        if self.match(TokenType.ELSE):
            else_body = self.stmt()
        else:
            else_body = Block([])

        return If(cond, then_body, else_body)

    def while_stmt(self) -> While:
        """
        while_stmt : "while" "(" expr ")" stmt
        """
        self.expect(TokenType.WHILE)
        self.expect(TokenType.LEFT_PAREN)
        cond = self.expr()
        self.expect(TokenType.RIGHT_PAREN)
        body = self.stmt()
        return While(cond, body)

    def for_stmt(self) -> Stmt:
        """
        for_stmt : "for" "(" var expr ";" expr ")" stmt


        for (init cond; incr) body

        =>

        {
            init
            while (cond) {
                body
                incr;
            }
        }
        """
        self.expect(TokenType.FOR)
        self.expect(TokenType.LEFT_PAREN)
        init = self.var()
        cond = self.expr()
        self.expect(TokenType.SEMICOLON)
        incr = self.expr()
        self.expect(TokenType.RIGHT_PAREN)
        body = self.stmt()

        return Block([
            init,
            While(cond, Block([
                body,
                ExprStmt(incr),
            ])),
        ])

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
