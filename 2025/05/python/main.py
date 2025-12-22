import fileinput

type IDRange = tuple[int, int]


class IDRanges(list[IDRange]):
    def check(self, num: int) -> bool:
        for low, high in self:
            if low <= num <= high:
                return True

        return False


def parse() -> tuple[IDRanges, list[int]]:
    id_ranges = IDRanges()
    nums: list[int] = []
    fp_input = fileinput.input()

    for line in fp_input:
        if len(line) == 1:
            break

        [low, high] = [int(n) for n in line[:-1].split("-")]
        id_ranges.append((low, high))

    for line in fp_input:
        nums.append(int(line[:-1]))

    return id_ranges, nums


if __name__ == "__main__":
    id_ranges, nums = parse()

    print(f"P1: {sum(id_ranges.check(num) for num in nums)}")
