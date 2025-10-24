import lark
from pathlib import Path
from typing import Any


GRAMMAR_FILE = Path(__file__).parent / "grammar.lark"
GRAMMAR_SOURCE = GRAMMAR_FILE.read_text()

grammar = lark.Lark(GRAMMAR_SOURCE, parser="lalr")


class JsonTransformer(lark.Transformer):
    def NUMBER(self, token: lark.Token):
        if "." in token:
            return float(token)
        return int(token)

    def STRING(self, token: lark.Token):
        return eval(str(token))

    def LITERAL(self, token: lark.Token):
        if token == "true":
            return True
        elif token == "false":
            return False
        elif token == "null":
            return None
        elif token == "Infinity":
            return float("inf")
        elif token == "-Infinity":
            return -float("inf")
        elif token == "NaN":
            return float("nan")
        else:
            raise ValueError(token)

    def array(self, data):
        # data = lista de filhos produzidos no simbolo não-terminal
        return data

    def object(self, data):
        # data = lista de members
        return dict(data)

    def member(self, data):
        [nome, valor] = data
        return (nome, valor)


def read_json(src: str) -> Any:
    transformer = JsonTransformer()
    tree = grammar.parse(src)
    data = transformer.transform(tree)
    return data


if __name__ == "__main__":
    import sys
    from pprint import pprint

    with open(sys.argv[1]) as f:
        source = f.read()
    result = read_json(source)
    print(type(result))
    pprint(result)
