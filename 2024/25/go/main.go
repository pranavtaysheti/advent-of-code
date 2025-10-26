package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"slices"
)

const patternLen = 7
const patternWidth = 5

type patternType int

const (
	ptLock patternType = iota
	ptKey
)

type pattern [patternLen][patternWidth]rune

func (p pattern) heightMap(spec patternType) []int {
	res := make([]int, patternWidth)
	switch spec {
	case ptLock:
		for i, row := range p {
			for j, c := range row {
				if c == '#' {
					res[j] = i + 1
				}
			}
		}
	case ptKey:
		var p_rev = pattern{}
		copy(p_rev[:], p[:])
		slices.Reverse(p_rev[:])
		for i, row := range p_rev {
			for j, c := range row {
				if c == '#' {
					res[j] = i + 1
				}
			}
		}
	}

	return res
}

type schematics struct {
	locks []pattern
	keys  []pattern
}

var data = schematics{
	locks: []pattern{},
	keys:  []pattern{},
}

func (s schematics) solve() (res int) {
	for _, l := range data.locks {
		hm_l := l.heightMap(ptLock)

	key:
		for _, k := range data.keys {
			hm_k := k.heightMap(ptKey)
			for i, h := range hm_k {
				if hm_l[i]+h > patternLen {
					continue key
				}
			}

			res++
		}
	}

	return
}

func parse(r io.Reader) {
	checkFilled := func(r [patternWidth]rune) bool {
		for _, c := range r {
			if c != '#' {
				return false
			}
		}

		return true
	}

	scanner := bufio.NewScanner(r)

	var curr pattern
	for i := 0; scanner.Scan(); i++ {
		line := scanner.Text()

		if i%(patternLen+1) == 0 {
			curr = pattern{}
		}

		if i%(patternLen+1) != patternLen {
			curr[i%(patternLen+1)] = [5]rune([]rune(line))
		}

		if i%(patternLen+1) == patternLen-1 {
			switch {
			case checkFilled(curr[0]):
				data.locks = append(data.locks, curr)
			case checkFilled(curr[patternLen-1]):
				data.keys = append(data.keys, curr)
			}
		}
	}

	fmt.Println(len(data.locks) + len(data.keys))
}

func main() {
	parse(os.Stdin)

	P1 := data.solve()
	P2 := 0

	fmt.Printf("P1: %d\n", P1)
	fmt.Printf("P2: %d\n", P2)
}
