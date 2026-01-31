import fileinput
from collections.abc import Sequence
from itertools import combinations


class Machine:
    _indicators: list[bool]
    _schematics: list[list[int]]
    _joltage: list[int]

    def __init__(
        self,
        indicators: list[bool],
        schematics: list[list[int]],
        joltage: list[int],
    ):
        self._indicators = indicators
        self._schematics = schematics
        self._joltage = joltage

    def _press(self, presses: Sequence[int]) -> bool:
        state = [False] * len(self._indicators)
        for p in presses:
            buttons = self._schematics[p]
            for b in buttons:
                state[b] = not state[b]

        return state == self._indicators

    def solve_toggle(self) -> tuple[int, ...]:
        for l in range(1, len(self._schematics)):
            for v in combinations(range(len(self._schematics)), l):
                if self._press(v):
                    return v

        raise AssertionError()

    def solve_sum(self) -> list[int]: ...


def parse():
    def process_line(l: str):
        s_indicators, *s_schematics, s_joltage = l.split()

        indicators = [True if s == "#" else False for s in s_indicators[1:-1]]
        schematics = [[int(n) for n in s[1:-1].split(",")] for s in s_schematics]
        joltage = [int(n) for n in s_joltage[1:-1].split(",")]

        return indicators, schematics, joltage

    return [Machine(*process_line(l)) for l in fileinput.input()]


if __name__ == "__main__":
    data = parse()
    print(f"P1: {sum(len(m.solve_toggle()) for m in data)}")
    print(f"P2: {0}")
