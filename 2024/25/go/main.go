package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
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

	case ptKey:
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

func (s schematics) solve() {

}

func parse(r io.Reader) {
	scanner := bufio.NewScanner(r)
	curr := pattern{}
	for i := 0; scanner.Scan(); i++ {
		line := scanner.Text()

		if i%(patternLen+1) == patternLen {
			switch {
			case curr[0] == [patternWidth]rune{'#', '#', '#', '#', '#'}:
				data.locks = append(data.locks, curr)
			case curr[patternLen-1] == [patternWidth]rune{'#', '#', '#', '#', '#'}:
				data.keys = append(data.keys, curr)
			}

			curr = pattern{}
			continue
		}

		curr[i%(patternLen+1)] = [5]rune([]rune(line))
	}
}

func main() {
	parse(os.Stdin)

	P1 := 0
	P2 := 0

	fmt.Printf("P1: %d\n", P1)
	fmt.Printf("P2: %d\n", P2)
}
