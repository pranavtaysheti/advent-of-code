import fileinput
import heapq

GRID_SIZE = 70
LENGTH = 1024

type Data = list[tuple[int, int]]


class Grid(list[list[bool]]):
    def __init__(self, data: Data):
        super().__init__(
            [[False for _ in range(GRID_SIZE + 1)] for _ in range(GRID_SIZE + 1)]
        )

        self.data = data
        for col, row in data[:LENGTH]:
            self[row][col] = True

    def __str__(self) -> str:
        str_map: dict[bool, str] = {True: "#", False: "."}
        return "\n".join("".join(str_map[c] for c in line) for line in self)

    def path_find(self) -> int:
        VECTORS = [(0, +1), (0, -1), (+1, 0), (-1, 0)]

        seen: set[tuple[int, int]] = set([(0, 0)])
        queue: list[tuple[int, tuple[int, int]]] = []

        queue.append((0, (0, 0)))
        while queue:
            curr_len, curr = heapq.heappop(queue)
            if curr == (GRID_SIZE, GRID_SIZE):
                break

            for d_row, d_col in VECTORS:
                c_row, c_col = curr
                n_row, n_col = c_row + d_row, c_col + d_col

                if (
                    ((0 <= n_row <= GRID_SIZE) and (0 <= n_col <= GRID_SIZE))
                    and ((n_row, n_col) not in seen)
                    and (not self[n_row][n_col])
                ):
                    heapq.heappush(queue, (curr_len + 1, (n_row, n_col)))
                    seen.add((n_row, n_col))

        else:
            return -1

        return curr_len

    def block_find(self) -> tuple[int, int]:
        for col, row in self.data[LENGTH:]:
            self[row][col] = True
            if self.path_find() == -1:
                return col, row

        raise AssertionError(
            "The path should have been blocked at some point, check input."
        )


data: list[tuple[int, int]] = []
with fileinput.input() as input_file:
    for line in input_file:
        num1, num2 = line.split(",")
        data.append((int(num1), int(num2)))

grid = Grid(data)

print(f"P1: {grid.path_find()}")
print(f"P2: {grid.block_find()}")
