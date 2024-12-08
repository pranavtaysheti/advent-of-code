package main

import (
	"bufio"
	"fmt"
	"io"
	"iter"
	"maps"
	"os"
	"slices"
)

type antennaMap map[[2]int]struct{}

func (a antennaMap) combinations() iter.Seq[[2][2]int] {
	return func(yield func([2][2]int) bool) {
		aSlice := slices.Collect(maps.Keys(a))

		for i := range len(aSlice) - 1 {
			for j := range len(aSlice) - 1 - i {
				if !yield([2][2]int{aSlice[i], aSlice[i+j+1]}) {
					return
				}
			}
		}
	}
}

func (a antennaMap) mapAntinodes() map[[2]int]struct{} {
	res := map[[2]int]struct{}{}

	for posPair := range a.combinations() {
		pos1, pos2 := posPair[0], posPair[1]
		cRow, cCol := pos2[0]-pos1[0], pos2[1]-pos1[1]

		antinodes := [2][2]int{
			{pos2[0] + cRow, pos2[1] + cCol},
			{pos1[0] - cRow, pos1[1] - cCol}}

		for _, an := range antinodes {
			if an[0] >= 0 && an[0] < size && an[1] >= 0 && an[1] < size {
				res[an] = struct{}{}
			}
		}
	}

	return res
}

var data = map[rune]antennaMap{}
var size = 0

func parse(r io.Reader) {
	scanner := bufio.NewScanner(r)

	for i := 0; scanner.Scan(); i++ {
		for j, c := range scanner.Text() {
			if c == '.' {
				continue
			}

			a, ok := data[c]
			if !ok {
				a = antennaMap{}
				data[c] = a
			}

			a[[2]int{i, j}] = struct{}{}
		}

		size = i+1
	}
}

func main() {
	parse(os.Stdin)
	antinodeMap := map[[2]int]struct{}{}
	for _, a := range data {
		maps.Copy(antinodeMap, a.mapAntinodes())
	}

	P1 := len(antinodeMap)
	P2 := 0

	fmt.Printf("P1: %d\n", P1)
	fmt.Printf("P2: %d\n", P2)
}
