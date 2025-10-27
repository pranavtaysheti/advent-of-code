import fileinput


class ExpandedDisk(list[int]):
    def __init__(self, layout: list[int]):
        super().__init__()

        for i, size in enumerate(layout):
            if i % 2 == 0:
                self.extend([i // 2 for _ in range(size)])
            else:
                self.extend([-1 for _ in range(size)])

    def compress(self):
        curr_blank = 0
        for i, e in enumerate(reversed(self)):
            if e == -1:
                continue

            while self[curr_blank] != -1:
                curr_blank += 1

            if len(self) - 1 - i <= curr_blank:
                break

            self[curr_blank] = e
            self[-1 - i] = -1

        del self[curr_blank:]

    def checksum(self) -> int:
        return sum(i * e for i, e in enumerate(self))

    def defragement(self): ...


with fileinput.input() as input_file:
    line = input_file.readline()[:-1]
    data = [int(c) for c in line]

compress_disk = ExpandedDisk(data)
compress_disk.compress()
print(f"P1: {compress_disk.checksum()}")

defragment_disk = ExpandedDisk(data)
defragment_disk.defragement()
print(f"P2: {defragment_disk.checksum()}")
