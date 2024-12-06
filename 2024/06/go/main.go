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
	if (p[0] >= 0 && p[0] < len(region)) &&
		(p[1] >= 0 && p[1] < len(region[0])) {
		return true
	}

	return false
}

type cursor struct {
	position
	direction
}

var region = [][]bool{}

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

		region = append(region, row)
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
			if region[pos[0]][pos[1]] == true {
				curr.direction = (curr.direction + 1) % 4
			}
		}

		curr.position = getNextPos()
	}

	return len(visitedMap)
}

// func countSteps() (steps int) {
// 	curr := start

// 	nextObstacle := func(line []bool) int {
// 		for i, o := range line {
// 			if o {
// 				return i
// 			}
// 		}

// 		return len(line) + 1
// 	}

// 	for curr.check() {
// 		var line []bool

// 		switch curr.direction {
// 		case dUp:
// 			for i := range curr.position[0] {
// 				line = append(line, region[curr.position[0]-1-i][curr.position[1]])
// 			}

// 		case dRight:
// 			line = region[curr.position[0]][curr.position[1]+1:]

// 		case dDown:
// 			for i := range len(region) - curr.position[0] - 1 {
// 				line = append(line, region[curr.position[0]+1+i][curr.position[1]])
// 			}

// 		case dLeft:
// 			line = slices.Clone(region[curr.position[0]][:curr.position[1]])
// 			slices.Reverse(line)
// 		}

// 		lineSteps := nextObstacle(line)

// 		curr.position = [2]int{
// 			curr.position[0] + lineSteps*curr.vector()[0],
// 			curr.position[1] + lineSteps*curr.vector()[1]}
// 		curr.direction = (curr.direction + 1) % 4

// 		steps += lineSteps
// 	}

// 	return
// }

func main() {
	parse(os.Stdin)

	P1 := solve()
	P2 := 0

	fmt.Printf("P1: %d\n", P1)
	fmt.Printf("P2: %d\n", P2)
}
