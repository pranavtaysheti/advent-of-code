import fileinput
from collections.abc import Generator
from fileinput import FileInput
from itertools import takewhile
from typing import NamedTuple


class Condition(NamedTuple):
    category: str
    operator: str
    limit: int


class Part(dict[str, int]):
    def score(self) -> int:
        return sum(self.values())


class Rule(NamedTuple):
    condition: Condition | None
    action: bool | str

    def test(self, part: Part) -> bool | str | None:
        if (
            (c := self.condition) is None
            or (c.operator == ">" and part[c.category] > c.limit)
            or (c.operator == "<" and part[c.category] < c.limit)
        ):
            return self.action


workflows: dict[str, list[Rule]] = {}
parts: list[Part] = []


def solve() -> Generator[Part]:
    def run_workflow(name: str, part: Part) -> bool:
        for rule in workflows[name]:
            if (res := rule.test(part)) is None:
                continue

            if isinstance(res, bool):
                return res

            return run_workflow(res, part)

        raise AssertionError("non-terminating workflow")

    return (part for part in parts if run_workflow("in", part))


def parse_input(file: FileInput[str]):
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
            if any((pos := condition.find(operator := o)) >= 0 for o in ["<", ">"]):
                return Condition(condition[:pos], operator, int(condition[pos + 1 :]))

            raise AssertionError

        def parse_rule(rule: str) -> Rule:
            if (index := rule.find(":")) == -1:
                return Rule(None, parse_action(rule))

            condition, action = rule[:index], rule[index + 1 :]
            return Rule(parse_condition(condition), parse_action(action))

        name = line[: line.index("{")]
        workflows[name] = [
            parse_rule(rule) for rule in line[len(name) + 1 : -2].split(",")
        ]

    def parse_part(line: str):
        part = Part()

        for cat_str in line[1:-2].split(","):
            category, amount = cat_str.split("=")
            part[category] = int(amount)

        parts.append(part)

    for line in takewhile(lambda l: len(l) > 1, file):
        parse_workflow(line)

    for line in file:
        parse_part(line)


parse_input(fileinput.input(encoding="utf-8"))

P1 = sum(p.score() for p in solve())
P2 = 0

print(f"P1: {P1}")
print(f"P2: {P2}")
