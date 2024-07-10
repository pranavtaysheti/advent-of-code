import fileinput
from ast import Or
from enum import Enum, StrEnum, auto
from itertools import chain
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


class Direction(Enum):
    UP = auto()
    RIGHT = auto()
    DOWN = auto()
    LEFT = auto()


class Orientation(Enum):
    HORIZONTAL = auto()
    VERTICAL = auto()


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


def solve(pos: Coordinate, direction: Direction) -> int:
    state: State = [[False for _ in range(len(data[0]))] for _ in range(len(data))]
    rays: list[Ray] = [Ray(pos, direction)]
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
        ray_state: dict[Orientation, list[Coordinate]] = {
            Orientation.HORIZONTAL: [],
            Orientation.VERTICAL: [],
        }
        curr_pos = ray.pos
        curr_direction = ray.direction

        def append_pos(pos: Coordinate, direction: Direction):
            ray_state[
                {
                    Direction.UP: Orientation.VERTICAL,
                    Direction.DOWN: Orientation.VERTICAL,
                    Direction.RIGHT: Orientation.HORIZONTAL,
                    Direction.LEFT: Orientation.HORIZONTAL,
                }[direction]
            ].append(pos)

        def step(pos: Coordinate, direction: Direction) -> Direction | None:
            append_pos(pos, direction)
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
            and (curr_pos not in ray_state)
        ):
            # print(f"{curr_pos.row=}, {curr_pos.col=}")

            curr_direction = step(curr_pos, curr_direction)
            if curr_direction is None:
                break

            curr_pos = next_pos(curr_pos, curr_direction)

        return ray_state

    while rays:
        ray_state = trace_ray(rays.pop())
        for row, col in chain(
            ray_state[Orientation.HORIZONTAL], ray_state[Orientation.VERTICAL]
        ):
            state[row][col] = True

    return sum(row.count(True) for row in state)


def main():
    global data

    with fileinput.input(encoding="utf8") as input_file:
        data = parse_input(input_file)

    P1: int = solve(Coordinate(0, 0), Direction.RIGHT)
    P2: int = max(
        *(solve(Coordinate(i, 0), Direction.RIGHT) for i in range(len(data))),
        *(solve(Coordinate(0, j), Direction.DOWN) for j in range(len(data[0]))),
        *(
            solve(Coordinate(i, len(data[0]) - 1), Direction.LEFT)
            for i in range(len(data))
        ),
        *(
            solve(Coordinate(len(data) - 1, j), Direction.UP)
            for j in range(len(data[0]))
        ),
    )

    print(f"P1: {P1}")
    print(f"P2: {P2}")


if __name__ == "__main__":
    main()
