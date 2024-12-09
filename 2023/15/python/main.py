import fileinput
from dataclasses import dataclass, field
from enum import StrEnum
from itertools import takewhile
from typing import NamedTuple


class Operation(StrEnum):
    DASH = "-"
    EQUAL = "="


class Record(NamedTuple):
    label: str
    operation: Operation
    focal_len: int | None


class Lens(NamedTuple):
    label: str
    focal_len: int


type Box = list[Lens]
type Data = list[Step]

data: Data


@dataclass
class Step:
    data: str
    record: Record = field(init=False)

    def __post_init__(self):
        self.record = self._parse()

    def _parse(self) -> Record:
        label = "".join([*takewhile(lambda c: c not in Operation, self.data)])
        operation = Operation(self.data[len(label)])
        focal_len = (
            int(self.data[len(label) + 1 :]) if operation == Operation.EQUAL else None
        )

        return Record(label, operation, focal_len)

    @classmethod
    def _hash(cls, string):
        curr: int = 0
        for c in string:
            curr += ord(c)
            curr *= 17
            curr %= 256

        return curr

    def step_hash(self) -> int:
        return self._hash(self.data)

    def label_hash(self) -> int:
        return self._hash(self.record.label)


def parse_input(input: fileinput.FileInput[str]) -> Data:
    return [Step(s) for s in next(input)[:-1].split(",")]


def hashmap() -> list[Box]:
    res: list[Box] = [[] for _ in range(256)]

    def process(step: Step):
        box = res[step.label_hash()]

        def remove_lens():
            for i, lens in enumerate(box):
                if lens.label == step.record.label:
                    box.pop(i)

        def replace_lens():
            assert step.record.focal_len is not None
            new_lens = Lens(step.record.label, step.record.focal_len)

            for i, lens in enumerate(box):
                if lens.label == new_lens.label:
                    box[i] = new_lens
                    return

            box.append(new_lens)

        match step.record.operation:
            case Operation.DASH:
                remove_lens()
            case Operation.EQUAL:
                replace_lens()

    for step in data:
        process(step)

    return res


def focal_power(pos: int, box: Box) -> int:
    def lens_power(pos: int, lens: Lens) -> int:
        return (pos + 1) * lens.focal_len

    return sum(lens_power(i, l) for i, l in enumerate(box)) * (pos + 1)


def main():
    global data

    with fileinput.input(encoding="utf8") as input_file:
        data = parse_input(input_file)

    P1: int = sum(s.step_hash() for s in data)
    P2: int = sum(focal_power(i, box) for i, box in enumerate(hashmap()))

    print(f"P1: {P1}")
    print(f"P2: {P2}")


if __name__ == "__main__":
    main()
