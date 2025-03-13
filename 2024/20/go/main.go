package main

import (
	"bufio"
	"fmt"
	"io"
	"math"
	"os"
	"strings"
)

const MIN_TIME = 100

type vector [2]int

var directions = [4]vector{
	{-1, 0},
	{0, +1},
	{+1, 0},
	{0, -1},
}

func (v vector) addTo(pos [2]int) [2]int {
	row, col := pos[0], pos[1]
	c_row, c_col := v[0], v[1]

	return [2]int{row + c_row, col + c_col}
}

type raceTrack struct {
	start [2]int
	end   [2]int
	track [][]int
}

type cheat struct {
	start [2]int
	end   [2]int
}

func (r raceTrack) prime() {
	for i, c := 0, r.start; c != r.end; i++ {
		for _, d := range directions {
			n_pos := d.addTo(c)
			n_row, n_col := n_pos[0], n_pos[1]

			if r.track[n_row][n_col] == 0 {
				r.track[n_row][n_col] = i + 1
				c = [2]int{n_row, n_col}
				break
			}
		}
	}
}

func (r raceTrack) findCheats() map[int]int {
	res := map[int]int{}

	for row, line := range r.track[1 : len(r.track)-1] {
		row = row + 1
		for col, e := range line[1 : len(line)-1] {
			col = col + 1
			if e < math.MaxInt {
				continue
			}

			for i, d := range directions[:2] {
				s1_pos := d.addTo([2]int{row, col})
				s1_row, s1_col := s1_pos[0], s1_pos[1]

				s2_pos := directions[i+2].addTo([2]int{row, col})
				s2_row, s2_col := s2_pos[0], s2_pos[1]

				s1 := r.track[s1_row][s1_col]
				s2 := r.track[s2_row][s2_col]

				if s1 < math.MaxInt && s2 < math.MaxInt {
					diff := max(s1, s2) - min(s1, s2)
					if v, ok := res[diff-2]; !ok {
						res[diff-2] = 1
					} else {
						res[diff-2] = v + 1
					}
				}
			}
		}
	}

	return res
}

func parse(r io.Reader) (m raceTrack) {
	scanner := bufio.NewScanner(r)

	for i := 0; scanner.Scan(); i++ {
		line := scanner.Text()

		if j := strings.IndexRune(line, 'S'); j > -1 {
			m.start = [2]int{i, j}
		}

		if j := strings.IndexRune(line, 'E'); j > -1 {
			m.end = [2]int{i, j}
		}

		m.track = append(m.track, make([]int, len(line)))
		for j, r := range line {
			if r == '#' {
				m.track[i][j] = math.MaxInt
			} else {
				m.track[i][j] = 0
			}
		}

	}

	return
}

func main() {
	data := parse(os.Stdin)
	data.prime()

	sum := 0
	for time, q := range data.findCheats() {
		if time >= 100 {
			sum += q
		}
	}

	P1 := sum
	P2 := 0

	fmt.Printf("P1: %d\n", P1)
	fmt.Printf("P2: %d\n", P2)
}
