package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"slices"
)

type expandedDisk []int

func expand(input []int) (d expandedDisk) {
	size := 0
	for _, length := range input {
		size += length
	}

	d = make([]int, size)

	curr := 0
	for i, length := range input {
		if i%2 == 0 {
			for j := range length {
				d[curr+j] = i / 2
			}
		} else {
			for j := range length {
				d[curr+j] = -1
			}
		}

		curr += length
	}

	return
}

func (d *expandedDisk) fragment() {
	currBlank := 0
	for i, e := range slices.Backward(*d) {
		if e == -1 {
			continue
		}

		for (*d)[currBlank] != -1 {
			currBlank++
		}

		if i <= currBlank {
			break
		}

		(*d)[currBlank] = e
		(*d)[i] = -1
	}

	*d = (*d)[:currBlank]
}

func (d expandedDisk) checksum() (res int) {
	for i, id := range d {
		res += i * id
	}

	return
}

func parse(r io.Reader) (res []int) {
	scanner := bufio.NewScanner(r)
	scanner.Scan()
	input := scanner.Text()

	res = make([]int, len(input))
	for i, r := range input {
		res[i] = int(r) - 48
	}

	return
}

func main() {
	data := parse(os.Stdin)

	diskState := expand(data)
	diskState.fragment()
	fmt.Printf("P1: %d\n", diskState.checksum())
	fmt.Printf("P2: %d\n", 0)
}
