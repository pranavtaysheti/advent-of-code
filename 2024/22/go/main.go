package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"strconv"
)

const histLen = 4
const pruneNumber = 16777216 - 1
const snGenerated = 2000

type number int

func (sn number) evolve() number {
	n_sn := sn << 6
	sn = n_sn ^ sn
	sn = sn & pruneNumber

	n_sn = sn >> 5
	sn = n_sn ^ sn
	sn = sn & pruneNumber

	n_sn = sn << 11
	sn = n_sn ^ sn
	sn = sn & pruneNumber

	return sn
}

func (sn number) generate() []number {
	res := make([]number, snGenerated+1)
	res[0] = sn
	for i := range snGenerated {
		sn = sn.evolve()
		res[i+1] = sn
	}

	return res
}

type sellReport map[[histLen]int8]int

func (s sellReport) maxProfit() int {
	currMax := 0
	for _, p := range s {
		currMax = max(currMax, p)
	}

	return currMax
}

type priceList []number

func (l priceList) observe() sellReport {
	curr := [histLen]int8{}
	res := sellReport{}

	//Prime the initial 4 numbers
	for i := range histLen {
		curr[i] = int8(l[i+1]%10 - l[i]%10)
	}

	fmt.Println("PRIMED SUCCESSFULLY:", curr)
	res[curr] = int(l[histLen] % 10)

	//Rest of the numbers
	for i := range len(l) - histLen - 1 {
		for j := range histLen - 1 {
			curr[j] = curr[j+1]
		}

		curr[histLen-1] = int8(l[histLen+i+1]%10 - l[histLen+i]%10)

		if v, ok := res[curr]; !ok {
			res[curr] = int(l[histLen+i+1] % 10)
		} else {
			res[curr] = v + int(l[histLen+i+1]%10)
		}
	}

	return res
}

var numbers []number

func parse(r io.Reader) {
	scanner := bufio.NewScanner(r)
	for scanner.Scan() {
		num, _ := strconv.Atoi(scanner.Text())
		numbers = append(numbers, number(num))
	}
}

func main() {
	parse(os.Stdin)

	P1 := 0
	for _, n := range numbers {
		generatedNumbers := n.generate()
		P1 += int(generatedNumbers[len(generatedNumbers)-1])
	}

	fmt.Printf("P1: %d\n", P1)

	P2 := 0
	fmt.Printf("P2: %d\n", P2)
}
