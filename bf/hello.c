
#include <stdio.h>

int main() {
    char tape[10000];
    int pos = 0;
    for (int i = 0; i < 10000; i++) {
        tape[i] = 0;
    }

    tape[pos]++;
    tape[pos]++;
    tape[pos]++;
    tape[pos]++;
    tape[pos]++;
    tape[pos]++;
    tape[pos]++;
    tape[pos]++;
    while (tape[pos] != 0) {
    pos++;
    tape[pos]++;
    tape[pos]++;
    tape[pos]++;
    tape[pos]++;
    while (tape[pos] != 0) {
    pos++;
    tape[pos]++;
    tape[pos]++;
    pos++;
    tape[pos]++;
    tape[pos]++;
    tape[pos]++;
    pos++;
    tape[pos]++;
    tape[pos]++;
    tape[pos]++;
    pos++;
    tape[pos]++;
    pos--;
    pos--;
    pos--;
    pos--;
    tape[pos]--;
    }
    pos++;
    tape[pos]++;
    pos++;
    tape[pos]++;
    pos++;
    tape[pos]--;
    pos++;
    pos++;
    tape[pos]++;
    while (tape[pos] != 0) {
    pos--;
    }
    pos--;
    tape[pos]--;
    }
    pos++;
    pos++;
    putchar(tape[pos]);
    pos++;
    tape[pos]--;
    tape[pos]--;
    tape[pos]--;
    putchar(tape[pos]);
    tape[pos]++;
    tape[pos]++;
    tape[pos]++;
    tape[pos]++;
    tape[pos]++;
    tape[pos]++;
    tape[pos]++;
    putchar(tape[pos]);
    putchar(tape[pos]);
    tape[pos]++;
    tape[pos]++;
    tape[pos]++;
    putchar(tape[pos]);
    pos++;
    pos++;
    putchar(tape[pos]);
    pos--;
    tape[pos]--;
    putchar(tape[pos]);
    pos--;
    putchar(tape[pos]);
    tape[pos]++;
    tape[pos]++;
    tape[pos]++;
    putchar(tape[pos]);
    tape[pos]--;
    tape[pos]--;
    tape[pos]--;
    tape[pos]--;
    tape[pos]--;
    tape[pos]--;
    putchar(tape[pos]);
    tape[pos]--;
    tape[pos]--;
    tape[pos]--;
    tape[pos]--;
    tape[pos]--;
    tape[pos]--;
    tape[pos]--;
    tape[pos]--;
    putchar(tape[pos]);
    pos++;
    pos++;
    tape[pos]++;
    putchar(tape[pos]);
    pos++;
    tape[pos]++;
    tape[pos]++;
    putchar(tape[pos]);
    return 0;
}

