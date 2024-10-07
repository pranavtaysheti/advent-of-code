package main

import (
	"bufio"
	"fmt"
	"io"
	"iter"
	"os"
	"slices"
	"strconv"
	"strings"
)

type record struct {
	springs []rune
	counts  []int
}

func (r record) expand() record {
	springs := make([]rune, len(r.springs)*5+4)
	counts := make([]int, len(r.counts)*5)

	for range 5 {
		springs = append(springs, r.springs...)
		springs = append(springs, '?')
		counts = append(counts, r.counts...)
	}

	return record{springs[:len(springs)-1], counts}
}

func (r record) solve() int {
	memo := memo{}
	return memo.solve(r.springs, r.counts, false)
}

type recordSlice []record

func (rSlice recordSlice) expandIter() iter.Seq[record] {
	return func(yield func(record) bool) {
		for _, r := range rSlice {
			if !yield(r.expand()) {
				return
			}
		}
	}
}

type memo struct{}

func (m memo) solve(s []rune, c []int, active bool) int {
	if len(c) == 1 && c[0] == 0 {
		c = []int{}
	}

	if len(s) == 0 && len(c) > 0 {
		return 0
	}

	if len(s) == 0 && len(c) == 0 {
		return 1
	}

	switch s[0] {
	case '#':
		if len(c) == 0 || (c[0] == 0 && active) {
			return 0
		}

		c[0] -= 1
		active = true

	case '.':
		if active {
			if c[0] > 0 {
				return 0
			}

			active = false
			c = c[1:]
		}

	case '?':
		damaged := m.solve(append([]rune{'#'}, s[1:]...), c, active)
		operational := m.solve(append([]rune{'.'}, s[1:]...), c, active)

		return damaged + operational
	}

	return m.solve(s[1:], c, active)
}

var data = recordSlice{}

func parseInput(r io.Reader) {
	scanner := bufio.NewScanner(r)

	for scanner.Scan() {
		fields := strings.Fields(scanner.Text())
		springsText := fields[0]
		countsTextSlice := strings.Split(fields[1], ",")

		counts := []int{}
		for _, c := range countsTextSlice {
			count, _ := strconv.Atoi(c)
			counts = append(counts, count)
		}

		springs := []rune{}
		for _, c := range springsText {
			springs = append(springs, c)
		}

		data = append(data, record{springs, counts})
	}
}

func solve(rSlice iter.Seq[record]) (res int) {
	for r := range rSlice {
		res += r.solve()
	}

	return
}

func main() {
	parseInput(os.Stdin)

	P1 := solve(slices.Values(data))
	// P2 := solve(data.expandIter())
	P2 := 0

	fmt.Printf("P1 %d \n", P1)
	fmt.Printf("P2 %d \n", P2)
}
