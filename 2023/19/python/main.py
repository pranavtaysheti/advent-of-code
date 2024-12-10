import fileinput
from copy import copy
from fileinput import FileInput
from itertools import takewhile
from typing import Literal, NamedTuple, Self

type Action = str | bool


class Part(dict[str, int]):
    def score(self) -> int:
        return sum(self.values())

    def check(self) -> bool:
        curr = workflows["in"]
        while not isinstance(action := curr.run(self), bool):
            curr = workflows[action]

        return action


class Condition(NamedTuple):
    category: str
    operator: Literal["<"] | Literal[">"]
    limit: int

    def test(self, part: Part) -> bool:
        if (self.operator == ">" and part[self.category] > self.limit) or (
            self.operator == "<" and part[self.category] < self.limit
        ):
            return True

        return False


class Rule(NamedTuple):
    condition: Condition | None
    action: Action

    def test(self, part) -> Action | None:
        if self.condition is None or self.condition.test(part):
            return self.action


class Range(NamedTuple):
    low: int
    high: int


class PartRange(dict[str, Range]):
    def split(self, condition: Condition) -> tuple[Self, Self]:
        accept, reject = copy(self), copy(self)

        o_range = self[condition.category]
        match condition.operator:
            case "<":
                accept[condition.category] = Range(o_range.low, condition.limit - 1)
                reject[condition.category] = Range(condition.limit, o_range.high)
            case ">":
                accept[condition.category] = Range(condition.limit + 1, o_range.high)
                reject[condition.category] = Range(o_range.low, condition.limit)

        return accept, reject


class WorkFlow(list[Rule]):
    def run(self, part: Part) -> Action:
        for rule in self:
            if (res := rule.test(part)) is not None:
                return res

        raise AssertionError("Non redirecting or terminating workflow")


workflows: dict[str, WorkFlow] = {}
parts: list[Part] = []


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
            if any((pos := condition.find(operator := o)) != -1 for o in ("<", ">")):
                return Condition(condition[:pos], operator, int(condition[pos + 1 :]))

            raise AssertionError(f"unknown operator: {operator}")

        def parse_rule(rule: str) -> Rule:
            if (index := rule.find(":")) == -1:
                return Rule(None, parse_action(rule))

            condition, action = rule[:index], rule[index + 1 :]
            return Rule(parse_condition(condition), parse_action(action))

        name = line[: line.index("{")]
        workflows[name] = WorkFlow(
            parse_rule(rule) for rule in line[len(name) + 1 : -2].split(",")
        )

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

P1 = sum(p.score() for p in parts if p.check())
P2 = 0

print(f"P1: {P1}")
print(f"P2: {P2}")
