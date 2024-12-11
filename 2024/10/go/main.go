package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
)

type topography [][]int

func (t topography) score(pos [2]int) (score int, rating int) {
	vectors := [][2]int{{-1, 0}, {0, +1}, {+1, 0}, {0, -1}}
	seen := map[[2]int]struct{}{}

	poi := [][2]int{pos}
	for len(poi) > 0 {
		currPos := poi[len(poi)-1]
		curr := t[currPos[0]][currPos[1]]
		poi = poi[:len(poi)-1]

		for _, v := range vectors {
			n_row, n_col := currPos[0]+v[0], currPos[1]+v[1]
			if n_row >= len(t) || n_row < 0 || n_col >= len(t[0]) || n_col < 0 {
				continue
			}

			next := t[n_row][n_col]

			if next == curr+1 {

				if next == 9 {
					if _, ok := seen[[2]int{n_row, n_col}]; !ok {
						seen[[2]int{n_row, n_col}] = struct{}{}
						score++
					}

					rating++
				} else {
					poi = append(poi, [2]int{n_row, n_col})
				}

			}
		}
	}

	return
}

func (t topography) solve() (score int, rating int) {
	for pos := range starts {
		n_score, n_rating := t.score(pos)
		score += n_score
		rating += n_rating
	}

	return
}

var data = topography{}
var starts = map[[2]int]struct{}{}

func parse(r io.Reader) {
	scanner := bufio.NewScanner(r)

	for i := 0; scanner.Scan(); i++ {
		data = append(data, []int{})

		for j, num := range scanner.Text() {
			data[i] = append(data[i], int(num)-48)
			if int(num)-48 == 0 {
				starts[[2]int{i, j}] = struct{}{}
			}
		}
	}
}

func main() {
	parse(os.Stdin)
	score, rating := data.solve()

	P1 := score
	P2 := rating

	fmt.Printf("P1: %d\n", P1)
	fmt.Printf("P2: %d\n", P2)
}
