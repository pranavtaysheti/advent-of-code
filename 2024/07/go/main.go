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
	tabulation map[int]bool
}

func (e *equation) solve() {
	e.tabulation = map[int]bool{}
	e.tabulation[e.numbers[0]] = false

	for _, num := range e.numbers[1:] {
		newTabulation := map[int]bool{}
		for res, isconcat := range e.tabulation {
			newTabulation[res+num] = isconcat
			newTabulation[res*num] = isconcat

			concatNum, _ := strconv.Atoi(fmt.Sprintf("%d%d", res, num))
			newTabulation[concatNum] = true
		}

		e.tabulation = newTabulation
	}
}

func (e equation) isSovled() (ok bool, usesConcat bool) {
	usesConcat, ok = e.tabulation[e.result]
	return
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

	woConcat := 0
	wConcat := 0

	for _, e := range data {
		(&e).solve()

		e.isSovled()
		if ok, usesConcat := e.isSovled(); ok {
			if usesConcat {
				wConcat += e.result
			} else {
				woConcat += e.result
			}
		}
	}

	P1 := woConcat
	P2 := wConcat + woConcat

	fmt.Printf("P1: %d\n", P1)
	fmt.Printf("P2: %d\n", P2)
}
