import fileinput
from array import array
from enum import IntEnum, StrEnum
from typing import NamedTuple


class Cell(StrEnum):
    SPACE = "."
    FORWARD_MIRROR = "/"
    BACKWARD_MIRROR = "\\"
    VERTICAL_SPLITTER = "|"
    HORIZONTAL_SPLLITTER = "-"


class Coordinate(NamedTuple):
    row: int
    col: int


class Direction(IntEnum):
    UP = 0
    RIGHT = 2
    DOWN = 1
    LEFT = 3


class Ray(NamedTuple):
    pos: Coordinate
    direction: Direction


type Energized = bool
type Data = list[list[Cell]]
type State = list[list[Energized]]
data: Data


def parse_input(input: fileinput.FileInput[str]) -> Data:
    res: Data = []
    for line in input:
        res.append([Cell(c) for c in line[:-1]])

    return res


def solve():
    state: State = [[False for _ in range(len(data[0]))] for _ in range(len(data))]
    rays: list[Ray] = [Ray(Coordinate(0, 0), Direction.RIGHT)]
    seen_splitters: list[Coordinate] = []

    def seen_splitter(pos: Coordinate) -> bool:
        if pos in seen_splitters:
            return True

        seen_splitters.append(pos)
        return False

    def add_ray(pos: Coordinate, direction: Direction):
        rays.append(Ray(next_pos(pos, direction), direction))

    def next_pos(pos: Coordinate, direction: Direction) -> Coordinate:
        match direction:
            case Direction.UP:
                return Coordinate(pos.row - 1, pos.col)
            case Direction.RIGHT:
                return Coordinate(pos.row, pos.col + 1)
            case Direction.DOWN:
                return Coordinate(pos.row + 1, pos.col)
            case Direction.LEFT:
                return Coordinate(pos.row, pos.col - 1)

    def trace_ray(ray: Ray):
        ray_state: State = [
            [False for _ in range(len(data[0]))] for _ in range(len(data))
        ]
        curr_pos = ray.pos
        curr_direction = ray.direction

        def step(pos: Coordinate, direction: Direction) -> Direction | None:
            ray_state[pos.row][pos.col] = True
            cell = data[pos.row][pos.col]

            match cell:
                case Cell.SPACE:
                    return direction

                case Cell.FORWARD_MIRROR:
                    return {
                        Direction.RIGHT: Direction.UP,
                        Direction.DOWN: Direction.LEFT,
                        Direction.UP: Direction.RIGHT,
                        Direction.LEFT: Direction.DOWN,
                    }[direction]

                case Cell.BACKWARD_MIRROR:
                    return {
                        Direction.RIGHT: Direction.DOWN,
                        Direction.DOWN: Direction.RIGHT,
                        Direction.UP: Direction.LEFT,
                        Direction.LEFT: Direction.UP,
                    }[direction]

                case Cell.VERTICAL_SPLITTER:
                    if direction in [Direction.UP, Direction.DOWN]:
                        return direction

                    if not seen_splitter(pos):
                        add_ray(pos, Direction.UP)
                        add_ray(pos, Direction.DOWN)

                case Cell.HORIZONTAL_SPLLITTER:
                    if direction in [Direction.RIGHT, Direction.LEFT]:
                        return direction

                    if not seen_splitter(pos):
                        add_ray(pos, Direction.RIGHT)
                        add_ray(pos, Direction.LEFT)

        while (
            (0 <= curr_pos.row < len(data))
            and (0 <= curr_pos.col < len(data[0]))
            and (not ray_state[curr_pos.row][curr_pos.col])
        ):
            # print(f"{curr_pos.row=}, {curr_pos.col=}")

            curr_direction = step(curr_pos, curr_direction)
            if curr_direction is None:
                break

            curr_pos = next_pos(curr_pos, curr_direction)

        return ray_state

    while rays:
        curr_state = trace_ray(rays.pop())
        state = [
            [
                any([curr_state[row][col], state[row][col]])
                for col in range(len(state[0]))
            ]
            for row in range(len(state))
        ]

    return state


def count_steps(state: State) -> int:
    return sum(row.count(True) for row in state)


def main():
    global data

    with fileinput.input(encoding="utf8") as input_file:
        data = parse_input(input_file)

    P1: int = count_steps(solve())
    P2: int = 0

    print(f"P1: {P1}")
    print(f"P2: {P2}")


if __name__ == "__main__":
    main()
