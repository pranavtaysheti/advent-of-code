package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
)

type direction int

const (
	dUp direction = iota
	dRight
	dDown
	dLeft
)

func (d direction) vector() [2]int {
	switch d {
	case dUp:
		return [2]int{-1, 0}
	case dRight:
		return [2]int{0, 1}
	case dDown:
		return [2]int{1, 0}
	case dLeft:
		return [2]int{0, -1}
	}

	panic(fmt.Sprint("unknown direction: ", d))
}

type position [2]int

func (p position) check() bool {
	if (p[0] >= 0 && p[0] < len(data)) &&
		(p[1] >= 0 && p[1] < len(data[0])) {
		return true
	}

	return false
}

type cursor struct {
	position
	direction
}

type region [][]bool


var data = region([][]bool{})

var start = cursor{}

func parse(r io.Reader) {
	scanner := bufio.NewScanner(r)

	for i := 0; scanner.Scan(); i++ {
		row := []bool{}
		for j, r := range scanner.Text() {
			if r == '#' {
				row = append(row, true)
			} else {
				if r == '.' {
					goto appendRow
				}

				switch r {
				case '^':
					start.direction = dUp
				case '>':
					start.direction = dRight
				case 'v':
					start.direction = dDown
				case '<':
					start.direction = dLeft
				}

				start.position = [2]int{i, j}

			appendRow:
				row = append(row, false)
			}
		}

		data = append(data, row)
	}
}

func solve() int {
	curr := start
	visitedMap := map[[2]int]struct{}{}

	getNextPos := func() position {
		return [2]int{
			curr.position[0] + curr.vector()[0],
			curr.position[1] + curr.vector()[1]}
	}

	for curr.check() {

		if _, ok := visitedMap[curr.position]; !ok {
			visitedMap[curr.position] = struct{}{}
		}

		if pos := getNextPos(); pos.check() {
			if data[pos[0]][pos[1]] == true {
				curr.direction = (curr.direction + 1) % 4
			}
		}

		curr.position = getNextPos()
	}

	return len(visitedMap)
}

func countLoop() {
	//TODO
}

func main() {
	parse(os.Stdin)

	P1 := solve()
	P2 := 0

	fmt.Printf("P1: %d\n", P1)
	fmt.Printf("P2: %d\n", P2)
}
