from dataclasses import dataclass
from string import ascii_letters, digits

type JSON = str | int | list["JSON"] | dict[str, "JSON"]

STRING_CHARS = {
    *ascii_letters,
    *digits,
    " ", "!", "#", "$", "%", "&", "'", "(", ")", "*", "_",
}

def read_json(source: str) -> JSON:
    parser = Parser(source)
    value = parser.value()
    if parser.position != len(source):
        raise ValueError("Extra data after JSON value")
    return value 

@dataclass
class Parser:
    source: str
    position: int = 0

    def value(self) -> JSON:
        self.ws()
        match self.peek():
            case '[':
                value = self.array()
            case '{':
                value = self.object()
            case "t":
                self.literal("true")
                value = True
            case "f":
                self.literal("false")
                value = False
            case "n":
                self.literal("null")
                value = None
            case '"':
                value = self.string()
            case c if c in "0123456789":
                value = self.number()
            case x:
                raise ValueError(f"Unexpected character: {x!r}")
        
        self.ws()
        return value

    def array(self) -> list[JSON]:
        self.read('[')
        self.ws()
        items = []

        # Lista vazia
        if self.peek() == ']':
            self.position += 1
            return items
        
        # Le o primeiro elemento
        value = self.value()
        items.append(value)

        # Le os elementos seguintes
        while self.peek() == ',':
            self.position += 1
            value = self.value()
            items.append(value)

        self.read(']')
        return items

    def object(self) -> dict[str, JSON]:
        self.read('{')
        self.ws()
        items = {}

        # Objeto vazio
        if self.peek() == '}':
            self.position += 1
            return items
        
        # Le o primeiro elemento
        self.ws()
        key = self.string()
        self.ws()
        self.read(':')
        value = self.value()
        items[key] = value

        # Le os elementos seguintes
        while self.peek() == ',':
            self.position += 1
            self.ws()
            key = self.string()
            self.ws()
            self.read(':')
            value = self.value()
            items[key] = value

        self.read('}')
        return items

    def string(self) -> str:
        chars = []
        self.read('"')
        while self.peek() in STRING_CHARS:
            chars.append(self.peek())
            self.position += 1
        self.read('"')
        return "".join(chars)

    def number(self) -> int:
        chars = []
        while self.peek() in "0123456789":
            chars.append(self.peek())
            self.position += 1
        text = "".join(chars)
        return int(text)
    
    def ws(self) -> None:
        while self.peek() in " \t\n\r":
            self.position += 1

    def peek(self) -> str:
        if self.position < len(self.source):
            return self.source[self.position]
        return "\0"
    
    def read(self, expected: str) -> None:
        if self.position >= len(self.source):
            raise ValueError("Unexpected end of input")
        if self.source[self.position] != expected:
            raise ValueError(f"Expected {expected!r}, got {self.source[self.position]!r}")
        self.position += 1

    def literal(self, text: str) -> None:
        if self.source.startswith(text, self.position):
            self.position += len(text)
        else:
            raise ValueError(f"Expected {text!r}")

if __name__ == "__main__":
    import sys
    from pprint import pprint

    with open(sys.argv[1]) as f:
        source = f.read()
    result = read_json(source)
    print(type(result))
    pprint(result)