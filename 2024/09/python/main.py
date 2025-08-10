from __future__ import annotations

import fileinput
from collections import deque
from itertools import islice

with fileinput.input() as input_file:
    line = input_file.readline()[:-1]
    data: list[int] = [int(c) for c in line]


class ExpandedDisk(list[int]):
    def __init__(self, layout: Layout):
        super().__init__()

        for num, length in layout:
            self.extend(num for _ in range(length))

    def compress(self) -> list[int]:
        blank = -1
        for i, e in enumerate(reversed(self)):
            if e == -1:
                continue

            i = len(self) - 1 - i

            for j, c in enumerate(islice(self, blank + 1, None)):
                if c == -1:
                    blank = blank + 1 + j
                    break

            if i <= blank:
                break

            self[blank] = e
            self[i] = -1

        self = self[: i + 1]  # type: ignore
        return self

    def checksum(self) -> int:
        return sum(i * e for i, e in enumerate(self.compress()))


class Layout(deque[tuple[int, int]]):
    def __init__(self, disk: list[int]):
        for i, length in enumerate(disk):
            if i % 2 == 0:
                self.append((i // 2, length))
            else:
                self.append((-1, length))

    def defragment(self):
        curr = len(self) // 2

        while curr >= 1:
            print(self)
            for i, (e_num, e_len) in enumerate(reversed(self)):
                i = len(self) - 1 - i

                if e_num == curr:
                    self[i] = (-1, e_len)
                    break

            curr -= 1

            if e_num == -1:
                continue

            for i, (num, length) in enumerate(self):
                if num == e_num:
                    break
                if (length > e_len) and num == -1:
                    break

            else:
                self.append((e_num, e_len))
                continue

            if num == e_num:
                continue

            self.insert(i, (e_num, e_len))  # type: ignore
            self.insert(i + 1, (-1, length - e_len))  # type: ignore
            del self[i + 2]


layout = Layout(data)

print(f"P1: {ExpandedDisk(layout).checksum()}")

print(layout)
layout.defragment()
print(ExpandedDisk(layout).checksum())
print(f"P2: {0}")
