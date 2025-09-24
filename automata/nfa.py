type State = int
type Msg = str


class NFA:
    initial: State = 0
    final: set[State] = {3, 4}
    transitions: dict[State, dict[Msg| None, set[State]]] = {
        0: {
            "a": {1},
            "b": {2},
            "c": {2},
        },
        1: {
            "b": {2, 3},
        },
        2: {
            "a": {2, 4},
            None: {1},
        },
        3: {
            None: {4},
        },
        4: {
            None: {0},
        },
    }


    def accept(self, text: str) -> bool:
        """
        Valida um texto segundo a linguagem definida pelo autômato.
        """
        states = {self.initial}
        self._add_epsilon_closure(states)

        for symbol in text:
            new_states = set()
            for state in states:
                try:
                    new_states.update(self.transitions[state][symbol])
                except KeyError:
                    continue
            self._add_epsilon_closure(new_states)

            states = new_states

        return bool(states.intersection(self.final))

    def _add_epsilon_closure(self, states: set[State]):
        """
        Propaga todos os estados epsilon acessíveis diretamente a
        partir da lista de estados inicial.

        Esse método propaga os epsilons de forma transitiva, assim se

        1 -> 2 por um epsilon e 2 -> 3, incluíremos tanto o estado 2
        quanto o estado 3 a partir de 1.
        """
        while True:
            n_states = len(states)
            for state in list(states):
                try:
                    states.update(self.transitions[state][None])
                except KeyError:
                    continue
            if n_states == len(states):
                return


if __name__ == "__main__":
    automaton = NFA()

    while True:
        try:
            text = input("> ")
        except (KeyboardInterrupt, EOFError):
            break

        if automaton.accept(text):
            print("🎉🎉")
        else:
            print("💩")

