package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
)

type position [2]int

type cursor struct {
	position
	vector [2]int
}

func (c *cursor) turn() {
	c.vector = [2]int{c.vector[1], -c.vector[0]}
}

func (c cursor) nextPos() [2]int {
	return [2]int{
		c.position[0] + c.vector[0],
		c.position[1] + c.vector[1]}
}

type region [][]bool

func (r region) isMapped(pos [2]int) bool {
	if (pos[0] >= 0 && pos[0] < len(r)) &&
		(pos[1] >= 0 && pos[1] < len(r[pos[0]])) {
		return true
	}

	return false
}

func (r region) solve() (visited map[[2]int]struct{}, isLoop bool) {
	curr := start
	visitedMap := map[[2]int]struct{}{}
	seenObstacles := map[[2]int]map[[2]int]struct{}{}

	for r.isMapped(curr.position) {
		for nextPos := curr.nextPos(); r.isMapped(nextPos) && r[nextPos[0]][nextPos[1]]; nextPos = curr.nextPos() {
			var seenVectors map[[2]int]struct{}

			if v, ok := seenObstacles[nextPos]; !ok {
				seenVectors = map[[2]int]struct{}{}
				seenObstacles[nextPos] = seenVectors
			} else {
				seenVectors = v
			}

			if _, ok := seenVectors[curr.vector]; ok {
				return visitedMap, true
			}

			seenVectors[curr.vector] = struct{}{}
			curr.turn()
		}

		visitedMap[curr.position] = struct{}{}
		curr.position = curr.nextPos()
	}

	return visitedMap, false
}

func (r region) solveWithObstacle(pos [2]int) (visited map[[2]int]struct{}, isLoop bool) {
	r[pos[0]][pos[1]] = true
	visited, isLoop = r.solve()
	r[pos[0]][pos[1]] = false
	return
}

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
				row = append(row, false)

				if r == '.' {
					continue
				}

				switch r {
				case '^':
					start.vector = [2]int{-1, 0}
				case '>':
					start.vector = [2]int{0, +1}
				case 'v':
					start.vector = [2]int{+1, 0}
				case '<':
					start.vector = [2]int{0, -1}
				}

				start.position = [2]int{i, j}
			}
		}

		data = append(data, row)
	}
}

func main() {
	parse(os.Stdin)

	visited, _ := data.solve()

	P1 := len(visited)
	
	P2 := 0
	for pos := range visited {
		if _, isLoop := data.solveWithObstacle(pos); isLoop {
			P2++
		}
	}

	fmt.Printf("P1: %d\n", P1)
	fmt.Printf("P2: %d\n", P2)
}
