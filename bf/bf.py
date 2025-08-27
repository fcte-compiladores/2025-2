import sys

def interpret(source: str):
    tape = [0] * 10000
    pos = 0
    ip = 0
    jump_points = []

    while ip < len(source):
        c = source[ip]
        match c:
            case "+":
                tape[pos] = (tape[pos] + 1) % 256
            case "-":
                tape[pos] = (tape[pos] - 1) % 256
            case ">":
                pos += 1
            case "<":
                pos -= 1
                if pos < 0:
                    raise IndexError("Tape position out of bounds")
            case ".":
                print(chr(tape[pos]), end="")
            case ",":
                tape[pos] = ord(sys.stdin.read(1)) if sys.stdin.isatty() else 0
            case "[" if tape[pos] == 0:
                ip = skip_loop(source, ip)
                continue
            case "[":
                jump_points.append(ip)
            case "]":
                ip = jump_points.pop()
                continue
        ip += 1

def skip_loop(source: str, ip: int) -> int:
    open_brackets = 1
    while open_brackets > 0:
        ip += 1
        if ip >= len(source):
            raise ValueError("Unmatched opening bracket")
        if source[ip] == "[":
            open_brackets += 1
        elif source[ip] == "]":
            open_brackets -= 1
    return ip + 1

def main():
    _, filename = sys.argv
    with open(filename, "r") as f:
        source = f.read()
    interpret(source)

if __name__ == "__main__":
    main()