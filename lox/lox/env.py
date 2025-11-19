from __future__ import annotations

from dataclasses import dataclass, field

from .ast import Value


@dataclass
class Env:
    parent: Env | None = None
    values: dict[str, Value] = field(default_factory=dict)

    def __getitem__(self, key: str) -> Value:
        try:
            return self.values[key]
        except KeyError:
            if self.parent is None:
                raise
            return self.parent[key]

    def __setitem__(self, key: str, value: Value):
        if key in self.values:
            self.values[key] = value
        elif self.parent is not None:
            self.parent[key] = value
        else:
            raise KeyError(key)

    def define(self, key: str, value: Value):
        if key in self.values:
            raise RuntimeError(f"redefinindo variável {key}.")
        self.values[key] = value

    def new_scope(self):
        return Env(self)