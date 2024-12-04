package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
)

type position struct {
	row int
	col int
}

var data = [][]rune{}
var posMap = map[rune]map[position]struct{}{}

func parse(r io.Reader) {
	scanner := bufio.NewScanner(r)

	for scanner.Scan() {
		data = append(data, []rune(scanner.Text()))
	}
}

func scan(rSlice ...rune) {
	runeMap := map[rune]struct{}{}
	for _, r := range rSlice {
		runeMap[r] = struct{}{}
	}

	for r := range runeMap {
		posMap[r] = map[position]struct{}{}
	}

	for i, row := range data {
		for j, cell := range row {
			if _, ok := runeMap[cell]; ok {
				posMap[cell][position{i, j}] = struct{}{}
			}
		}
	}
}

func linearSearch(w string) (res int) {
	vectors := [8][2]int{{1, 1}, {1, 0}, {1, -1}, {0, 1}, {0, -1}, {-1, 1}, {-1, 0}, {-1, -1}}
	for pos := range posMap[rune(w[0])] {
	vectorLoop:
		for _, v := range vectors {
			for i, r := range w {
				row := pos.row + v[0]*i
				if row >= len(data) || row < 0 {
					continue vectorLoop
				}

				col := pos.col + v[1]*i
				if col >= len(data[0]) || col < 0 {
					continue vectorLoop
				}

				if data[row][col] != r {
					continue vectorLoop
				}
			}

			res++
		}
	}

	return
}

func CrossSearch(center rune, corner1 rune, corner2 rune) (count int) {
	for pos := range posMap[center] {
		if pos.row == 0 || pos.col == 0 || pos.row == len(data)-1 || pos.col == len(data[0])-1 {
			continue
		}

		corners := []rune{}
		corners = append(corners, data[pos.row-1][pos.col-1])
		corners = append(corners, data[pos.row-1][pos.col+1])
		corners = append(corners, data[pos.row+1][pos.col+1])
		corners = append(corners, data[pos.row+1][pos.col-1])


		if (corners[0] == corners[1] && corners[2] == corners[3]) ||
			(corners[0] == corners[3] && corners[1] == corners[2]) {
			cornerMap := map[rune]struct{}{}
			for _, c := range corners {
				cornerMap[c] = struct{}{}
			}

			_, ok1 := cornerMap[corner1]
			_, ok2 := cornerMap[corner2]

			if ok1 && ok2 {
				count++
			}
		}
	}
	return
}
func main() {
	parse(os.Stdin)
	scan('X', 'A')

	P1 := linearSearch("XMAS")
	P2 := CrossSearch('A', 'M', 'S')

	fmt.Printf("P1: %d\n", P1)
	fmt.Printf("P2: %d\n", P2)
}
