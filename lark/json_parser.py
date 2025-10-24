import lark
from pathlib import Path
from typing import Any

GRAMMAR_FILE = Path(__file__).parent / "grammar.lark"
GRAMMAR_SOURCE = GRAMMAR_FILE.read_text()
GRAMMAR = lark.Lark(GRAMMAR_SOURCE, parser="lalr")

class JsonTransformer(lark.Transformer):
    def NUMBER(self, token: lark.Token):
        if "." not in token and "e" not in token and "E" not in token:
            return int(token)
        return float(token)

    def STRING(self, token: lark.Token):
        return eval(token)

    def LITERAL(self, token: lark.Token):
        if token == "true":
            return True
        elif token == "false":
            return False
        elif token == "null":
            return None
        raise ValueError(token)

    def array(self, children: list):
        return children

    def object(self, children: list):
        return dict(children)

    def pair(self, children):
        [name, value] = children
        return (name, value)

def read_json(src: str) -> Any:
    transformer = JsonTransformer()
    tree = GRAMMAR.parse(src)
    return transformer.transform(tree)


if __name__ == "__main__":
    import sys
    from pprint import pprint

    with open(sys.argv[1]) as f:
        source = f.read()
    result = read_json(source)
    print(type(result))
    pprint(result)
