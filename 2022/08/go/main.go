package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
)

type tree int

type forest [][]tree

func (f forest) isExposed(i int, j int) bool {
	if i == 0 || i == len(f)-1 || j == 0 || j == len(f[0])-1 {
		return true
	}

	vSlice := []tree{}
	for _, row := range f {
		vSlice = append(vSlice, row[j])
	}

	tEast := f[i][:j]
	tWest := f[i][j+1:]
	tNorth := vSlice[:i]
	tSouth := vSlice[i+1:]

outer:
	for _, tSlice := range [][]tree{tEast, tWest, tNorth, tSouth} {
		for _, tree := range tSlice {
			if int(tree) >= int(f[i][j]) {
				continue outer
			}
		}

		return true
	}

	return false
}

func (f forest) countExposed() (count int) {
	for i := range len(f) {
		for j := range len(f[0]) {
			if f.isExposed(i, j) {
				count++
			}
		}
	}

	return
}

var data forest

func parse(r io.Reader) {
	scanner := bufio.NewScanner(r)
	for i := 0; scanner.Scan(); i++ {
		data = append(data, []tree{})
		for _, char := range scanner.Text() {
			height := int(char) - 48
			data[i] = append(data[i], tree(height))
		}
	}
}

func main() {
	parse(os.Stdin)

	P1 := data.countExposed()
	P2 := 0

	fmt.Printf("P1: %d\n", P1)
	fmt.Printf("P2: %d\n", P2)
}
