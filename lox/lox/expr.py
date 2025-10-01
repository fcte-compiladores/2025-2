from dataclasses import dataclass

type Value = str | float | bool | None


class Expr:
    """
    Classe base abstrata de todas as expressões Lox
    """


@dataclass
class Literal(Expr):
    value: Value

    def eval(self) -> Value:
        return self.value


@dataclass
class Add(Expr):
    left: Expr
    right: Expr

    def eval(self) -> Value:
        return self.left.eval() + self.right.eval()  # type: ignore


@dataclass
class Sub(Expr):
    left: Expr
    right: Expr

    def eval(self) -> Value:
        return self.left.eval() - self.right.eval()  # type: ignore


@dataclass
class Mul(Expr):
    left: Expr
    right: Expr


@dataclass
class Div(Expr):
    left: Expr
    right: Expr
