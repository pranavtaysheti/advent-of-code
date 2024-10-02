import fileinput
from dataclasses import dataclass, field
from fileinput import FileInput
from itertools import takewhile
from typing import NamedTuple


class Condition(NamedTuple):
    category: str
    operator: str
    limit: int


class Rule(NamedTuple):
    condition: Condition | None
    action: bool | str

    def test(self, part) -> bool | str | None:
        if self.condition is None:
            return self.action

        c = self.condition
        match c.operator:
            case ">":
                if getattr(part, c.category) > c.limit:
                    return self.action

                return None

            case "<":
                if getattr(part, c.category) < c.limit:
                    return self.action

                return None


class Part(NamedTuple):
    x: int = 0
    m: int = 0
    a: int = 0
    s: int = 0

    def value(self) -> int:
        return self.x + self.m + self.a + self.s


@dataclass
class Data:
    workflows: dict[str, list[Rule]] = field(default_factory=dict)
    parts: list[Part] = field(default_factory=list)

    def solve(self) -> list[Part]:
        def run_workflow(name: str, part: Part) -> bool:
            for rule in self.workflows[name]:
                if (res := rule.test(part)) is None:
                    continue

                if isinstance(res, bool):
                    return res

                return run_workflow(res, part)

            raise AssertionError

        return [part for part in self.parts if run_workflow("in", part)]


def parse_input(file: FileInput[str]) -> Data:
    data = Data()

    def parse_workflow(line: str):
        def parse_action(action: str) -> bool | str:
            match action:
                case "A":
                    return True
                case "R":
                    return False
                case _:
                    return action

        def parse_condition(condition: str) -> Condition:
            if any((pos := condition.find(operator := o)) > 0 for o in ["<", ">"]):
                pos = condition.index(operator)
                return Condition(condition[:pos], operator, int(condition[pos + 1 :]))

            raise AssertionError

        def parse_rule(rule: str) -> Rule:
            if ":" not in rule:
                return Rule(None, parse_action(rule))

            condition, action = rule.split(":")
            return Rule(parse_condition(condition), parse_action(action))

        name = line[: line.index("{")]
        workflow = [parse_rule(rule) for rule in line[len(name) + 1 : -2].split(",")]
        data.workflows[name] = workflow

    def parse_part(line: str):
        numbers: list[int] = []
        for cat_str in line[1:-2].split(","):
            _, amount = cat_str.split("=")
            numbers.append(int(amount))

        data.parts.append(Part(*numbers))

    for line in takewhile(lambda l: len(l) > 1, file):
        parse_workflow(line)

    for line in file:
        parse_part(line)

    return data


if __name__ == "__main__":
    data = parse_input(fileinput.input(encoding="utf-8"))

    P1 = sum(p.value() for p in data.solve())
    P2 = 0

    print(f"P1: {P1}")
    print(f"P2: {P2}")
