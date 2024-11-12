import fileinput
from itertools import batched


class Item(str):
    def priority(self) -> int:
        v = ord(self)

        if 97 <= v <= 122:
            return v - 96
        if 65 <= v <= 90:
            return v - 64 + 26

        raise AssertionError(f"unexpected char {v}")


class RugSack(str):
    def common(self) -> Item:
        left = self[: len(self) // 2]
        right = self[len(self) // 2 :]

        (res,) = set(left).intersection(set(right))
        return Item(res)


class Group(list[RugSack]):
    def batch(self) -> Item:
        (res,) = set(self[0]).intersection(self[1]).intersection(self[2])
        return Item(res)


data: list[RugSack] = []
for line in fileinput.input():
    data.append(RugSack(line[:-1]))

print(f"P1: {sum(i.common().priority() for i in data)}")
print(f"P2: {sum(Group(b).batch().priority() for b in batched(data,3))}")
