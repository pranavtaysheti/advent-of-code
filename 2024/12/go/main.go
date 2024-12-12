package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
)

type farm [][]rune

var data = farm([][]rune{})

func (f farm) solve() (cost int) {
	seen := map[[2]int]struct{}{}

	for i, line := range data {
		for j := range line {
			if _, ok := seen[[2]int{i, j}]; !ok {
				region := f.fill([2]int{i, j})
				for pos := range region {
					seen[pos] = struct{}{}
				}

				area, perimeter := region.fencingCost()
				cost += area * perimeter
			}
		}
	}

	return
}

func (f farm) fill(pos [2]int) (r region) {
	r = make(region)
	plant := f[pos[0]][pos[1]]
	vectors := [4][2]int{{-1, 0}, {0, +1}, {+1, 0}, {0, -1}}

	poi := [][2]int{pos}
	for len(poi) > 0 {
		currPos := poi[len(poi)-1]
		r[currPos] = 0
		poi = poi[:len(poi)-1]

		for _, v := range vectors {
			nPos := [2]int{currPos[0] + v[0], currPos[1] + v[1]}
			if nPos[0] < 0 || nPos[0] >= len(f) ||
				nPos[1] < 0 || nPos[1] >= len(f[0]) {
				r[currPos]++
				continue
			}

			if f[nPos[0]][nPos[1]] == plant {
				if _, ok := r[nPos]; !ok {
					poi = append(poi, nPos)
				}
			} else {
				r[currPos]++
			}
		}
	}

	return
}

type region map[[2]int]int

func (r region) fencingCost() (area int, perimeter int) {
	for _, ends := range r {
		area++
		perimeter += ends
	}

	return
}

func parse(r io.Reader) {
	scanner := bufio.NewScanner(r)

	for i := 0; scanner.Scan(); i++ {
		data = append(data, []rune{})

		for _, r := range scanner.Text() {
			data[i] = append(data[i], r)
		}
	}
}

func main() {
	parse(os.Stdin)

	P1 := data.solve()
	P2 := 0

	fmt.Printf("P1: %d\n", P1)
	fmt.Printf("P2: %d\n", P2)
}
