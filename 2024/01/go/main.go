package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"slices"
	"strconv"
	"strings"
)

type lists [][]int

var data = lists(make([][]int, 2))

func parse(r io.Reader) {
	scanner := bufio.NewScanner(r)
	for scanner.Scan() {
		fields := strings.Fields(scanner.Text())
		num0, _ := strconv.Atoi(fields[0])
		num1, _ := strconv.Atoi(fields[1])

		data[0] = append(data[0], num0)
		data[1] = append(data[1], num1)
	}
}

func (l lists) similarityScore() (res int) {
	counts := map[int]int{}

	for _, n := range l[1] {
		_, ok := counts[n]
		if !ok {
			counts[n] = 0
		}

		counts[n] += 1
	}

	for _, n := range l[0] {
		if qty, ok := counts[n]; ok {
			res += qty*n
		}
	}

	return
}

func (l lists) solve() (res int) {
	slices.Sort(l[0])
	slices.Sort(l[1])

	for i := range len(l[0]) {
		diff := l[0][i] - l[1][i]
		if diff < 0 {
			diff = -diff
		}

		res += diff
	}

	return
}

func main() {
	parse(os.Stdin)

	P1 := data.solve()
	P2 := data.similarityScore()

	fmt.Printf("P1: %d\n", P1)
	fmt.Printf("P2: %d\n", P2)
}
