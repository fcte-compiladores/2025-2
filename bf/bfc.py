import sys


C_CODE = """
#include <stdio.h>

int main() {
    char tape[10000];
    int pos = 0;
    for (int i = 0; i < 10000; i++) {
        tape[i] = 0;
    }

// codigo bf
    return 0;
}
"""

def compile(source: str) -> str:
    def write(line):
        commands.append("    " + line)
    
    commands = []
    open_parens = 0
    for c in source:
        match c:
            case "+":
                write("tape[pos]++;")
            case "-":
                write("tape[pos]--;")
            case ">":
                write("pos++;")
            case "<":
                write("pos--;")
            case ".":
                write("putchar(tape[pos]);")
            case ",":
                write("tape[pos] = getchar();")
            case "[":
                write("while (tape[pos] != 0) {")
                open_parens += 1
            case "]":
                write("}")
                if open_parens == 0:
                    raise ValueError("Unmatched closing bracket")
                open_parens -= 1

    if open_parens != 0:
        raise ValueError("Unmatched opening bracket")

    c_code = C_CODE.replace("// codigo bf", "\n".join(commands))
    return c_code


def main():
    _, filename = sys.argv
    with open(filename, "r") as f:
        source = f.read()
    c_code = compile(source)
    print(c_code)


if __name__ == "__main__":
    main()