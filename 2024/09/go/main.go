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

func (d *expandedDisk) compress() {
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

func (d *expandedDisk) defragment() {
	trackedFile := -1
	fileStop, fileLen := -1, 0
	for i, e := range slices.Backward(*d) {
		if e == -1 {
			continue
		}

		if e == trackedFile {
			fileLen++
			continue
		}

		blankStart, blankLen := -1, 0
		for j, c := range (*d)[:fileStop-fileLen+2] {
			if c == -1 {
				if blankStart == -1 {
					blankStart = j
				}

				blankLen++
				continue
			}

			if blankLen >= fileLen {
				for k := range fileLen {
					(*d)[blankStart+k] = trackedFile
					(*d)[fileStop-k] = -1
				}

				break
			}

			blankStart, blankLen = -1, 0
		}

		trackedFile = e
		fileStop, fileLen = i, 1
	}
}

func (d expandedDisk) checksum() (res int) {
	for i, id := range d {
		if id == -1 {
			continue
		}

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

	compressState := expand(data)
	compressState.compress()
	fmt.Printf("P1: %d\n", compressState.checksum())

	deframentState := expand(data)
	deframentState.defragment()
	fmt.Printf("P2: %d\n", deframentState.checksum())
}
