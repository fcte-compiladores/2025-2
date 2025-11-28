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

    def get_at(self, key: str, position: int):
        if position > 0 and self.parent is not None:
            return self.parent.get_at(key, position - 1)
        return self.values[key]

    def set_at(self, key: str, position: int, value: Value):
        if position > 0 and self.parent is not None:
            return self.parent.set_at(key, position - 1, value)
        if position == 0:
            self.values[key] = value
        else:
            raise KeyError(key)

    def define(self, key: str, value: Value):
        if key in self.values:
            raise RuntimeError(f"redefinindo variável {key}.")
        self.values[key] = value

    def new_scope(self):
        return Env(self)