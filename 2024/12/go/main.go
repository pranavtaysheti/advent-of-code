package main

import (
	"bufio"
	"fmt"
	"io"
	"math/bits"
	"os"
	"slices"
)

type fenceType uint

const (
	ftVerLeft fenceType = 1 << iota
	ftVerRight
	ftHorTop
	ftHorBottom
)

func (ft fenceType) count() (count int) {
	return bits.OnesCount(uint(ft))
}

var vectors = map[fenceType][2]int{
	ftVerLeft:   {0, -1},
	ftVerRight:  {0, +1},
	ftHorTop:    {-1, 0},
	ftHorBottom: {+1, 0},
}

type region map[[2]int]fenceType

func (r region) peri() (res int) {
	for _, fenceType := range r {
		res += fenceType.count()
	}

	return
}

func (r region) sides() (res int) {
	vals := make([]uint, 0, 4*len(r))
	for pos, fence := range r {
		for _, ft := range []fenceType{ftVerLeft, ftVerRight} {
			if (ft & fence) > 0 {
				vals = append(vals, uint(ft<<16)+uint(pos[1]<<8)+uint(pos[0]))
			}
		}

		for _, ft := range []fenceType{ftHorBottom, ftHorTop} {
			if (ft & fence) > 0 {
				vals = append(vals, uint(ft<<16)+uint(pos[0]<<8)+uint(pos[1]))
			}
		}
	}

	slices.Sort(vals)

	var prev uint = 0
	for _, v := range vals {
		if v-prev != 1 {
			res++
		}
		prev = v
	}

	return
}

type farm [][]rune

func (f farm) solve() (res []region) {
	seen := make([][]bool, len(f))
	for i := range len(seen) {
		seen[i] = make([]bool, len(f[i]))
	}

	for i, line := range f {
		for j := range line {
			if seen[i][j] == false {
				reg := f.fill([2]int{i, j})
				for pos := range reg {
					seen[pos[0]][pos[1]] = true
				}

				res = append(res, reg)
			}
		}
	}

	return
}

func (f farm) fill(rootPos [2]int) (reg region) {
	reg = make(region)
	root := f[rootPos[0]][rootPos[1]]
	nextPos := [][2]int{rootPos}
	for len(nextPos) > 0 {
		currPos := nextPos[len(nextPos)-1]
		nextPos = nextPos[:len(nextPos)-1]

		for ft, v := range vectors {
			np := [2]int{currPos[0] + v[0], currPos[1] + v[1]}
			if np[0] < 0 {
				reg[currPos] |= ftHorTop
				continue
			}
			if np[0] >= len(f) {
				reg[currPos] |= ftHorBottom
				continue
			}
			if np[1] < 0 {
				reg[currPos] |= ftVerLeft
				continue
			}
			if np[1] >= len(f[0]) {
				reg[currPos] |= ftVerRight
				continue
			}

			if f[np[0]][np[1]] == root {
				if _, ok := reg[np]; !ok {
					nextPos = append(nextPos, np)
					reg[np] = 0
				}
			} else {
				reg[currPos] |= ft
			}
		}
	}

	return reg
}

func parse(r io.Reader) (res [][]rune) {
	scanner := bufio.NewScanner(r)
	for i := 0; scanner.Scan(); i++ {
		res = append(res, []rune{})

		for _, r := range scanner.Text() {
			res[i] = append(res[i], r)
		}
	}

	return res
}

func main() {
	data := parse(os.Stdin)
	farm := farm(data)

	P1 := 0
	for _, reg := range farm.solve() {
		area := len(reg)
		peri := reg.peri()

		P1 += area * peri
	}

	P2 := 0
	for _, reg := range farm.solve() {
		area := len(reg)
		sides := reg.sides()

		P2 += area * sides
	}

	fmt.Printf("P1: %d\n", P1)
	fmt.Printf("P2: %d\n", P2)
}
