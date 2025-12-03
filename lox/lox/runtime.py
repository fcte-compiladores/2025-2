from __future__ import annotations
import abc
from dataclasses import dataclass, field
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

    @property
    def name(self):
        return self.ast.name

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

    def bind(self, instance: LoxInstance):
        env = self.closure.new_scope()
        env.define("this", instance)
        return LoxFunction(self.ast, env)

    def __repr__(self):
        return f"fn {self.name}"


@dataclass
class LoxClass(LoxCallable):
    name: str
    superclass: LoxClass | None = None
    methods: dict[str, LoxFunction] = field(default_factory=dict)

    def call(self, ctx: Env, args: list[Value]):
        instance = LoxInstance(self)
        return instance

    def n_args(self) -> int:
        return 0

    def get_method(self, name: str) -> LoxFunction | None:
        return self.methods.get(name)

    def __repr__(self):
        return self.name

@dataclass
class LoxInstance:
    klass: LoxClass
    fields: dict[str, Value] = field(default_factory=dict)

    def getattr(self, attr: str) -> Value:
        try:
            return self.fields[attr]
        except KeyError:
            method = self.klass.get_method(attr)
            if method is None:
                raise RuntimeError(f"atributo {attr} não existe em {self}")
            return method.bind(self)

    def setattr(self, attr: str, value: Value):
        self.fields[attr] = value

    def __repr__(self):
        return f"{self.klass} instance"
