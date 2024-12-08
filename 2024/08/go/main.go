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

func (a antennaMap) mapAntinodes() map[[2]int]bool {
	res := map[[2]int]bool{}

	for posPair := range a.combinations() {
		pos1, pos2 := posPair[0], posPair[1]
		cRow, cCol := pos2[0]-pos1[0], pos2[1]-pos1[1]

		for i := 0; ; i++ {
			antinodes := [2][2]int{
				{pos2[0] + i*cRow, pos2[1] + i*cCol},
				{pos1[0] - i*cRow, pos1[1] - i*cCol}}

			rejected := 0
			for _, pos := range antinodes {
				if pos[0] >= 0 && pos[0] < size && pos[1] >= 0 && pos[1] < size {
					if i == 1 {
						res[pos] = true
					} else {
						if _, ok := res[pos]; !ok {
							res[pos] = false
						}
					}
				} else {
					rejected++
				}
			}

			if rejected == 2 {
				break
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

		size = i + 1
	}
}

func main() {
	parse(os.Stdin)

	antinodeMap := map[[2]int]struct{}{}
	firstHarmonic := map[[2]int]struct{}{}

	for _, a := range data {
		for pos, isFirst := range a.mapAntinodes() {
			if isFirst {
				firstHarmonic[pos] = struct{}{}
			}

			antinodeMap[pos] = struct{}{}
		}
	}

	P1 := len(firstHarmonic)
	P2 := len(antinodeMap)

	fmt.Printf("P1: %d\n", P1)
	fmt.Printf("P2: %d\n", P2)
}
