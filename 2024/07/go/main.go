package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"strconv"
	"strings"
)

type operator int

const (
	oMul operator = iota
	oAdd
)

type expression struct {
	left  int
	right int
	operator
}

type equation struct {
	result     int
	numbers    []int
	tabulation map[int]struct{}
}

func (e equation) solve() bool {
	e.tabulation = map[int]struct{}{}
	e.tabulation[e.numbers[0]] = struct{}{}

	for _, num := range e.numbers[1:] {
		newTabulation := map[int]struct{}{}
		for res := range e.tabulation {
			newTabulation[res+num] = struct{}{}
			newTabulation[res*num] = struct{}{}
		}

		e.tabulation = newTabulation
	}

	_, ok := e.tabulation[e.result]
	return ok
}

var data = []equation{}

func parse(r io.Reader) {
	scanner := bufio.NewScanner(r)

	for scanner.Scan() {
		fields := strings.Fields(scanner.Text())

		equation := equation{
			numbers: make([]int, len(fields)-1),
		}

		equation.result, _ = strconv.Atoi(fields[0][:len(fields[0])-1])
		for i, numStr := range fields[1:] {
			equation.numbers[i], _ = strconv.Atoi(numStr)
		}

		data = append(data, equation)
	}
}

func main() {
	parse(os.Stdin)

	P1 := 0
	for _, e := range data {
		if e.solve() {
			P1 += e.result
		}
	}

	P2 := 0

	fmt.Printf("P1: %d\n", P1)
	fmt.Printf("P2: %d\n", P2)
}
