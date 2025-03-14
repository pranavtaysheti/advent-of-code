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
	curr_blank := 0
	for i, e := range slices.Backward(*d) {
		if e == -1 {
			continue
		}

		for (*d)[curr_blank] != -1 {
			curr_blank++
		}

		if i <= curr_blank {
			break
		}

		(*d)[curr_blank] = e
		(*d)[i] = -1
	}

	*d = (*d)[:curr_blank]
}

func (s expandedDisk) checksum() (res int) {
	for i, id := range s {
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
	P1 := diskState.checksum()
	P2 := 0

	fmt.Printf("P1: %d\n", P1)
	fmt.Printf("P2: %d\n", P2)
}
