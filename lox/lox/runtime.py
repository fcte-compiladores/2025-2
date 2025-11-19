from __future__ import annotations
import abc
from dataclasses import dataclass
from typing import Callable, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .interpreter import Value, Env
    from .ast import Function


class LoxCallable(abc.ABC):
    @abc.abstractmethod
    def call(self, ctx: Env, args: list[Value]):
        raise NotImplementedError

    @abc.abstractmethod
    def n_args(self) -> int:
        raise NotImplementedError


@dataclass
class NativeFunction(LoxCallable):
    python_callable: Callable[..., Any]
    arity: int

    def n_args(self):
        return self.arity

    def call(self, ctx, args):
        return self.python_callable(*args)


@dataclass
class LoxFunction(LoxCallable):
    ast: Function
    closure: Env

    def n_args(self):
       return len(self.ast.params)

    def call(self, ctx: Env, argvalues: list[Value]):
        from .interpreter import exec, LoxReturn

        # Abre um novo escopo de variáveis
        ctx = self.closure.new_scope()

        # Insere os argumentos no escopo atual
        argnames = self.ast.params
        for name, value in zip(argnames, argvalues):
            ctx.define(name, value)

        # Excuta o corpo da função
        try:
            for stmt in self.ast.body:
                exec(stmt, ctx)
        except LoxReturn as exception:
            return exception.value

@dataclass
class LoxClass:
    name: str
    superclass: LoxClass | None
    methods: dict[str, LoxFunction]


@dataclass
class LoxInstance:
    fields: dict[str, Value]
    klass: LoxClass

