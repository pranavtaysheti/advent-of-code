import fileinput

type Data = list[str]
data: Data


def parse_input(input: fileinput.FileInput[str]) -> Data:
    return next(input)[:-1].split(",")


def hash(step: str) -> int:
    curr: int = 0

    for c in step:
        curr += ord(c)
        curr *= 17
        curr %= 256

    return curr


def main():
    global data

    with fileinput.input(encoding="utf8") as input_file:
        data = parse_input(input_file)

    P1: int = sum(hash(s) for s in data)
    P2: int = 0

    print(f"P1: {P1}")
    print(f"P2: {P2}")


if __name__ == "__main__":
    main()
