from typing import NamedTuple
import re

class Token(NamedTuple):
    type: str
    value: str
    line: int
    column: int

def tokenize(code):
    keywords = {'IF', 'THEN', 'ENDIF', 'FOR', 'NEXT', 'GOSUB', 'RETURN'}
    token_specification = [
        ('LEFT_PAREN', r"\("),
        ('RIGHT_PAREN', r"\)"),
        ('LEFT_BRACE', r"\{"),
        ('RIGHT_BRACE', r"\}"),
        ('COMMA', r","),
        ('DOT', r"\."),
        ('SEMICOLON', r";"),
        ('MINUS', r"-"),
        ('PLUS', r"\+"),
        ('SLASH', r"\/"),
        ('STAR', r"\*"),

        ('BANG_EQUAL', r"!="),
        ('BANG', r"!"),
        ('EQUAL_EQUAL', r"=="),
        ('EQUAL', r"="),
        ('GREATER_EQUAL', r">="),
        ('GREATER', r">"),
        ('LESS_EQUAL', r"<="),
        ('LESS', r"<"),

        ("NUMBER", r"([0-9]+(\.[0-9]+)?"),
        ("STRING", r"..."),
        ("IDENTIFIER", r"..."),

        # Simbolos especiais      # Arithmetic operators
        ('NEWLINE',  r'\n'),           # Line endings
        ('SKIP',     r'[ \t]+'),       # Skip over spaces and tabs
        ('MISMATCH', r'.'),            # Any other character
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    line_num = 1
    line_start = 0
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start
        if kind == 'NUMBER':
            value = float(value) if '.' in value else int(value)
        elif kind == 'ID' and value in keywords:
            kind = value
        elif kind == 'NEWLINE':
            line_start = mo.end()
            line_num += 1
            continue
        elif kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'{value!r} unexpected on line {line_num}')
        yield Token(kind, value, line_num, column)

statements = '''
    IF quantity THEN
        total := total + price * quantity;
        tax := price * 0.05;
    ENDIF;
'''

for token in tokenize(statements):
    print(token)