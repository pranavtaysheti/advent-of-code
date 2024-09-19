package main

//solved using modified djikstra algorithm. scope for optimization exists.
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
	stepFilter   func(a approach, d direction) bool
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

func (p *pathFinder) isNewNextBlock(pos position, a approach, s int) bool {
	for _, b := range p.nextBlocks {
		if b.approach == a && b.position == pos && b.shortestPath <= s {
			return false
		}
	}

	return true
}

func crucibleStepFilter(a approach, d direction) bool {
	if a.approachSteps == 3 && d == a.approachDirection {
		return false
	}

	return true
}

func ultraCrucibleStepFilter(a approach, d direction) bool {
	if (a.approachSteps == 10 && d == a.approachDirection) ||
		((a.approachSteps < 4 && a.approachSteps > 0) && d != a.approachDirection) {
		return false
	}

	return true
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

		return !(p.currApproach.approachDirection+d == 3)
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
		if !check(n.position, n.direction) || !p.stepFilter(p.currApproach, n.direction) {
			continue
		}

		approach, shortestPath := updateBlock(n.position, n.direction)
		if !p.isNewNextBlock(n.position, approach, shortestPath) || !p.memo.isNewApproach(n.position, approach) {
			continue
		}

		p.nextBlocks = append(p.nextBlocks, blockPos{n.position, shortestPath, approach})
	}

	return
}

func (m memo) isNewApproach(pos position, a approach) bool {
	if len(m[pos]) > 0 {
		for approach := range m[pos] {
			if approach == a {
				return false
			}
		}

		return true
	}

	m[pos] = map[approach]int{}
	return true
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

func (p *pathFinder) step() bool {
	p.updateNextBlocks()
	if b, ok := p.closestNextBlock(); ok {
		p.setNewApproach(b.position, b.approach, b.shortestPath)
		return true
	}

	return false
}

func (p *pathFinder) getShortest(pos position, f func(a approach) bool) int {
	res := math.MaxInt
	for approach, shortest := range p.memo[pos] {
		// fmt.Println(approach, shortest)
		if shortest < res && f(approach) {
			res = shortest
		}
	}

	// fmt.Println("-----------")
	return res
}

func crucibleSolFilter(_ approach) bool {
	return true
}

func ultraCrucibleSolFilter(a approach) bool {
	if a.approachSteps < 4 {
		return false
	}

	return true
}

func solvePathFinder(c func(a approach, d direction) bool) (res *pathFinder) {
	res = &pathFinder{
		memo:       memo{},
		stepFilter: c,
	}
	res.memo[position{0, 0}] = map[approach]int{}

	for res.step() {
	}

	return res
}

func main() {
	parseInput(os.Stdin)

	P1 := solvePathFinder(crucibleStepFilter).getShortest(position{len(data) - 1, len(data[0]) - 1}, crucibleSolFilter)
	P2 := solvePathFinder(ultraCrucibleStepFilter).getShortest(position{len(data) - 1, len(data[0]) - 1}, ultraCrucibleSolFilter)

	fmt.Printf("P1: %v \n", P1)
	fmt.Printf("P2: %d \n", P2)
}
