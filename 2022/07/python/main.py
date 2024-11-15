import fileinput
from functools import cached_property
from typing import Protocol, Self


class Node(Protocol):
    @cached_property
    def size(self) -> int: ...


class File(int):
    @cached_property
    def size(self) -> Self:
        return self


class Directory(dict[str, Node]):
    @cached_property
    def size(self) -> int:
        return sum(v.size for v in self.values())

    def walk(self) -> list[int]:
        res: list[int] = []
        for val in self.values():
            if isinstance(val, Directory):
                res.extend(val.walk())

        res.append(self.size)
        return res

    def smallest_dir(self, update: int, total_space: int) -> int:
        available_space = total_space - file_tree.size
        required_space = update - available_space
        for size in sorted(self.walk()):
            if size > required_space:
                return size

        raise AssertionError("No folder found.")


file_tree = Directory()

with fileinput.input() as input_file:
    path: list[Directory] = []
    curr_dir: Directory = file_tree

    for line in input_file:
        fields = line.split()

        if fields[0].isnumeric():
            curr_dir[fields[1]] = File(int(fields[0]))

        elif fields[0] == "dir":
            curr_dir[fields[1]] = Directory()

        elif fields[0] == "$":
            if fields[1] == "ls":
                continue

            if fields[2] == "/":
                curr_dir = file_tree
                path = []

            elif fields[2] == "..":
                curr_dir = path.pop()

            else:
                path.append(curr_dir)
                curr_dir = curr_dir[fields[2]]  # type: ignore

print(f"P1: {sum(filter(lambda s: s < 1_00_000, file_tree.walk()))}")
print(f"P2: {file_tree.smallest_dir(3_00_00_000, 7_00_00_000)}")
