package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"slices"
	"strconv"
)

type elf []int

func (e elf) sum() (res int) {
	for _, calories := range e {
		res += calories
	}

	return res
}

type elfSlice []elf

func (es elfSlice) sort() []int {
	sums := func() (res []int) {
		for _, e := range es {
			res = append(res, e.sum())
		}

		return
	}()

	slices.Sort(sums)
	slices.Reverse(sums)
	return sums
}

var data elfSlice

func parseInput(r io.Reader) {
	scanner := bufio.NewScanner(r)

	currElf := []int{}
	for scanner.Scan() {
		if scanner.Text() == "" {
			data = append(data, currElf)
			currElf = []int{}
		}

		calories, _ := strconv.Atoi(scanner.Text())
		currElf = append(currElf, calories)
	}

	data = append(data, currElf)
}

func main() {
	parseInput(os.Stdin)
	sorted := data.sort()

	P1 := sorted[0]
	P2 := sorted[0] + sorted[1] + sorted[2]

	fmt.Printf("P1: %d \n", P1)
	fmt.Printf("P2: %d \n", P2)
}
