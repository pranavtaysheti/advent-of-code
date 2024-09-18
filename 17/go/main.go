package main

import (
	"bufio"
	"fmt"
	"io"
	"math"
	"os"
	"slices"
	"strconv"
)

type direction int

const (
	dDown direction = iota
	dRight
	dLeft
	dUp
)

type approach struct {
	approachDirection direction
	approachSteps     int
}

type blockPos struct {
	position
	shortestPath int
	approach
}

type memo map[position]map[approach]int

type position struct {
	row int
	col int
}

type pathFinder struct {
	currBlockPos position
	currApproach approach
	currSteps    int
	memo         memo
	nextBlocks   []blockPos
}

var data [][]int

func parseInput(r io.Reader) {
	scanner := bufio.NewScanner(r)

	for scanner.Scan() {
		line := scanner.Text()

		parsedLine := []int{}
		for _, c := range line {
			num, _ := strconv.Atoi(string(c))
			parsedLine = append(parsedLine, num)
		}

		data = append(data, parsedLine)
	}

}

func (p *pathFinder) isInNextBlocks(pos position, a approach, s int) bool {
	for _, b := range p.nextBlocks {
		if b.approach == a && b.position == pos && b.shortestPath <= s {
			return true
		}
	}

	return false
}

func (p *pathFinder) updateNextBlocks() {
	newWeight := func(pos position) int {
		return p.currSteps + data[pos.row][pos.col]
	}

	approachSteps := func(d direction) int {
		if p.currApproach.approachDirection == d {
			return p.currApproach.approachSteps + 1
		}

		return 1
	}

	check := func(pos position, d direction) bool {
		if pos.row == len(data) || pos.row == -1 || pos.col == -1 || pos.col == len(data[0]) {
			return false
		}

		if p.currApproach.approachSteps == 3 && d == p.currApproach.approachDirection {
			return false
		}

		if p.currApproach.approachDirection+d == 3 {
			return false
		}

		return true
	}

	updateBlock := func(pos position, d direction) (a approach, s int) {
		return approach{
				approachDirection: d,
				approachSteps:     approachSteps(d),
			},
			newWeight(pos)
	}

	currRow := p.currBlockPos.row
	currCol := p.currBlockPos.col

	possiblities := []struct {
		position
		direction
	}{
		{position{currRow, currCol + 1}, dRight},
		{position{currRow, currCol - 1}, dLeft},
		{position{currRow + 1, currCol}, dDown},
		{position{currRow - 1, currCol}, dUp},
	}

	for _, n := range possiblities {
		if !check(n.position, n.direction) {
			continue
		}

		approach, shortestPath := updateBlock(n.position, n.direction)
		if p.isInNextBlocks(n.position, approach, shortestPath) || p.memo.isApproached(n.position, approach) {
			continue
		}

		p.nextBlocks = append(p.nextBlocks, blockPos{n.position, shortestPath, approach})
	}

	return
}

func (m memo) isApproached(pos position, a approach) bool {
	if len(m[pos]) > 0 {
		for approach := range m[pos] {
			if approach == a {
				return true
			}
		}

		return false
	}

	m[pos] = map[approach]int{}
	return false
}

func (m memo) addApproach(pos position, a approach, s int) {
	if len(m[pos]) == 0 {
		m[pos] = map[approach]int{}
		m[pos][a] = s
		return
	}

	if shortest, ok := m[pos][a]; ok {
		if s < shortest {
			m[pos][a] = s
		}
	} else {
		m[pos][a] = s
	}
}

func (p *pathFinder) closestNextBlock() (blockPos blockPos, ok bool) {
	shortestYet := math.MaxInt
	var blockIndex int

	for i, b := range p.nextBlocks {
		if b.shortestPath < shortestYet {
			shortestYet = b.shortestPath
			blockPos = b
			blockIndex = i
			ok = true
		}
	}

	if !ok {
		return
	}

	p.nextBlocks = slices.Delete(p.nextBlocks, blockIndex, blockIndex+1)
	return
}

func (p *pathFinder) setNewApproach(pos position, a approach, s int) {
	p.memo.addApproach(pos, a, s)
	p.currBlockPos = pos
	p.currApproach = a
	p.currSteps = s
}

func (p *pathFinder) solve() {
	p.updateNextBlocks()
	if b, ok := p.closestNextBlock(); ok {
		p.setNewApproach(b.position, b.approach, b.shortestPath)
		p.solve()
	}
}

func (p *pathFinder) getShortest(pos position) int {
	res := math.MaxInt
	for _, shortest := range p.memo[pos] {
		if shortest < res {
			res = shortest
		}
	}

	return res
}

func newPathFinder() (res pathFinder) {
	res = pathFinder{
		memo: memo{},
	}
	res.memo[position{0, 0}] = map[approach]int{}

	return res
}

func main() {
	parseInput(os.Stdin)
	pathFinder := newPathFinder()
	(&pathFinder).solve()

	P1 := pathFinder.getShortest(position{len(data) - 1, len(data[0]) - 1})
	P2 := 0

	fmt.Printf("P1: %v \n", P1)
	fmt.Printf("P2: %d \n", P2)
}
