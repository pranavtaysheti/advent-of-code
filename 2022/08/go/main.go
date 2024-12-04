package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"slices"
)

type tree int

type forest [][]tree

func (f forest) isExposed(i int, j int) (exposed bool, score int) {
	if i == 0 || i == len(f)-1 || j == 0 || j == len(f[0])-1 {
		return true, 0
	}

	vSlice := []tree{}
	for _, row := range f {
		vSlice = append(vSlice, row[j])
	}

	score = 1

	tEast :=  slices.Clone(f[i][:j])
	slices.Reverse(tEast)

	tWest := f[i][j+1:]
	
	tNorth := vSlice[:i]
	slices.Reverse(tNorth)

	tSouth := vSlice[i+1:]

	for _, tSlice := range [][]tree{tEast, tWest, tNorth, tSouth} {
		var q int
		var tree tree
		for q, tree = range tSlice {
			if int(tree) >= int(f[i][j]) {
				goto mulScore
			}
		}

		exposed = true

	mulScore:
		score *= q + 1
	}

	return
}

func (f forest) solve() (count int, maxScore int) {
	for i := range len(f) {
		for j := range len(f[0]) {
			exposed, score := f.isExposed(i, j)
			if exposed {
				count++
			}

			maxScore = max(maxScore, score)
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
	count, maxScore := data.solve()
	P1 := count
	P2 := maxScore

	fmt.Printf("P1: %d\n", P1)
	fmt.Printf("P2: %d\n", P2)
}
