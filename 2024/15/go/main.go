package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"slices"
	"strings"
)

var vector = map[rune][2]int{
	'^': {-1, 0},
	'>': {0, +1},
	'v': {+1, 0},
	'<': {0, -1},
}

func addVector(pos [2]int, vec [2]int) [2]int {
	return [2]int{pos[0] + vec[0], pos[1] + vec[1]}
}

type warehouse struct {
	instructions []rune
	floor        [][]rune
	cursor       [2]int
}

func (w warehouse) clone() state {
	clonedFloor := make([][]rune, len(w.floor))
	for i, r := range w.floor {
		clonedFloor[i] = slices.Clone(r)
	}

	return state{
		instructions: w.instructions,
		floor:        clonedFloor,
		cursor:       w.cursor,
	}
}

func (w warehouse) solve() state {
	state := w.clone()
	for i := range len(state.instructions) {
		state.move(i)
	}

	return state
}

func (w warehouse) expand() expandedState {
	clonedFloor := make([][]rune, len(w.floor))
	for i := range len(clonedFloor) {
		clonedFloor[i] = make([]rune, len(w.floor[i])*2)
		curr := clonedFloor[i]

		for j, r := range w.floor[i] {
			switch r {
			case 'O':
				curr[j*2], curr[j*2+1] = '[', ']'
			default:
				curr[j*2], curr[j*2+1] = r, r
			}

		}
	}

	return expandedState{
		instructions: w.instructions,
		floor:        clonedFloor,
		cursor:       [2]int{w.cursor[0] * 2, w.cursor[1] * 2},
	}
}

type state warehouse

func (w state) check(i int) (elems [][2]int, moves bool) {
	vec := vector[w.instructions[i]]

	curr := addVector(w.cursor, vec)
	for w.floor[curr[0]][curr[1]] == 'O' {
		elems = append(elems, curr)
		curr = addVector(curr, vec)
	}

	switch w.floor[curr[0]][curr[1]] {
	case '.':
		moves = true
	case '#':
		moves = false
	}

	return
}

func (w *state) move(i int) {
	elems, moves := w.check(i)
	if !moves {
		return
	}

	if len(elems) > 0 {
		start := elems[0]
		end := addVector(elems[len(elems)-1], vector[w.instructions[i]])

		w.floor[start[0]][start[1]] = '.'
		w.floor[end[0]][end[1]] = 'O'
	}

	w.cursor = addVector(w.cursor, vector[w.instructions[i]])
}

func (w state) gpsScore() (res int) {
	for i, row := range w.floor {
		for j, c := range row {
			if c == 'O' {
				res += 100*i + j
			}
		}
	}

	return
}

type expandedState warehouse

func (w expandedState) check(i int) (elems [][2]int, moves bool) {
	vec := vector[w.instructions[i]]

	// next := func(pos [][2]int) [][2]int {
	// 	switch {
	// 	case vec[0] == 0:
	// 		return [][2]int{addVector(w.cursor, vec)}
	// 	case vec[1] == 0:

	// 	}
	// }
}

func (w expandedState) move(i int) {
	// TODO
}

var data = warehouse{}

func parse(r io.Reader) {
	scanner := bufio.NewScanner(r)

	for i := 0; scanner.Scan(); i++ {
		if len(scanner.Text()) == 0 {
			break
		}

		line := []rune(scanner.Text())
		if j := strings.IndexRune(scanner.Text(), '@'); j >= 0 {
			data.cursor = [2]int{i, j}
			line[j] = '.'
		}

		data.floor = append(data.floor, line)
	}

	for scanner.Scan() {
		data.instructions = append(data.instructions, []rune(scanner.Text())...)
	}
}

func main() {
	parse(os.Stdin)

	P1 := data.solve().gpsScore()
	P2 := 0

	data.expand()
	fmt.Printf("P1: %d\n", P1)
	fmt.Printf("P2: %d\n", P2)
}
