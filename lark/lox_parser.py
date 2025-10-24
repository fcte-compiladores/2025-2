import lark
from pathlib import Path
from typing import Any


GRAMMAR_FILE = Path(__file__).parent / "lox.lark"
GRAMMAR_SOURCE = GRAMMAR_FILE.read_text()

grammar = lark.Lark(GRAMMAR_SOURCE, parser="lalr", start="program")


class LoxTransformer(lark.Transformer):
    ...

def parse_lox(src: str) -> Any:
    transformer = LoxTransformer()
    tree = grammar.parse(src)
    print(tree.pretty())
    data = transformer.transform(tree)
    print("-" * 40)
    print(data.pretty())
    return data


if __name__ == "__main__":
    import sys
    from pprint import pprint

    with open(sys.argv[1]) as f:
        source = f.read()
    result = parse_lox(source)
    print(type(result))
    pprint(result)
