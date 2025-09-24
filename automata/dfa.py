type State = int
type Msg = str


class DFA:
    initial: State = 0
    final: set[State] = {3, 4}
    transitions: dict[State, dict[Msg, State]] = {
        0: {
            "a": 1,
            "b": 2,
            "c": 2,
        },
        1: {
            "b": 3,
        },
        2: {
            "a": 4,
        },
    }


    def accept(self, text: str) -> bool:
        """
        Valida um texto segundo a linguagem definida pelo autômato.
        """
        state = self.initial

        for symbol in text:
            try:
                state = self.transitions[state][symbol]
            except KeyError:
                return False

        return state in self.final



if __name__ == "__main__":
    automaton = DFA()

    while True:
        try:
            text = input("> ")
        except (KeyboardInterrupt, EOFError):
            break

        if text == "":
            break
        elif automaton.accept(text):
            print("🎉🎉")
        else:
            print("💩")

