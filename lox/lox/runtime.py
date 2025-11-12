from __future__ import annotations
import abc
from dataclasses import dataclass
from typing import Callable, Any, TYPE_CHECKING
from .ast import Function

if TYPE_CHECKING:
    from .interpreter import Value, Env


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

    def n_args(self):
       return len(self.ast.params)

    def call(self, ctx: Env, args: list[Value]):
        ...

@dataclass
class LoxClass:
    name: str
    superclass: LoxClass | None
    methods: dict[str, LoxFunction]


@dataclass
class LoxIntance:
    fields: dict[str, Value]
    klass: LoxClass

