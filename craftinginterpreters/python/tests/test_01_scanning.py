"""
This test module assumes that lox:tokenize or lox.scanner:tokenize is available
and has the signature `tokenize(str) -> list[Token]`.

The tokens should have a __str__ method that produces a representation like:

    <TokenType> <lexeme> <literal>

It may contain additional information, but that will be ignored by the tests.
"""

from functools import cached_property
from itertools import count
from pathlib import Path
from typing import Iterator

from lox.testing import Example, example, mod

TEST_BASE = Path(__file__).parent.parent / "examples" / "scanning"


class ScannerBase:
    file: str

    @cached_property
    def example(self) -> Example:
        path = TEST_BASE / f"{self.file}.lox"
        return example(path)

    def expected_tokens(self) -> Iterator[str]:
        for line in self.example.output_lines():
            yield normalize_token_representation(line)

    def scan_tokens(self) -> Iterator[str]:
        tokenize = mod("scanner:tokenize")

        for token in tokenize(self.example.source):
            yield normalize_token_representation(str(token))

    def test_scanner(self):
        parsed = self.scan_tokens()
        answers = self.expected_tokens()
        for i, got, expected in zip(count(1), parsed, answers):
            if got == expected or got.startswith(expected):
                continue
            assert got == expected, f"line {i}: got {got!r}, expected {expected!r}"


class TestIdentifiers(ScannerBase):
    file = "identifiers"


class TestKeywords(ScannerBase):
    file = "keywords"


class TestNumbers(ScannerBase):
    file = "numbers"


class TestPunctuation(ScannerBase):
    file = "punctuators"


class TestStrings(ScannerBase):
    file = "strings"


class TestWhitesoace(ScannerBase):
    file = "whitespace"


def normalize_token_representation(line: str) -> str:
    if line.endswith("null"):
        line = line[:-4] + "None"
    line = line.replace("'", "").rstrip()
    return line
