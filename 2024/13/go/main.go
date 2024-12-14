package main

import (
	"bufio"
	"fmt"
	"io"
	"math"
	"os"
	"strconv"
	"strings"
)

type clawMachine struct {
	buttonA [2]int
	buttonB [2]int
	Prize   [2]int
}

func (c clawMachine) calculate() (push [2]int, ok bool) {
	denominator := c.buttonA[1]*c.buttonB[0] - c.buttonA[0]*c.buttonB[1]
	numeratorA := c.Prize[0]*c.buttonB[1] - c.Prize[1]*c.buttonB[0]
	numeratorB := c.Prize[0]*c.buttonA[1] - c.Prize[1]*c.buttonA[0]

	pushA := float64(numeratorA) / float64(-denominator)
	pushB := float64(numeratorB) / float64(denominator)

	return [2]int{int(pushA), int(pushB)},
		(pushA == math.Ceil(pushA)) && (pushB == math.Ceil(pushB))
}

func (c clawMachine) correct(factor int) clawMachine {
	newClawMachine := c
	newClawMachine.Prize[0] = factor + newClawMachine.Prize[0]
	newClawMachine.Prize[1] = factor + newClawMachine.Prize[1]

	return newClawMachine
}

func (c clawMachine) tokens(costA int, costB int) int {
	push, ok := c.calculate()
	if ok {
		return push[0]*costA + push[1]*costB
	}

	return 0
}

var data = []clawMachine{}

func parse(r io.Reader) {
	scanner := bufio.NewScanner(r)

	curr := clawMachine{}
	for i := 0; scanner.Scan(); i++ {
		fields := strings.Fields(scanner.Text())

		switch i % 4 {
		case 0:
			num1, _ := strconv.Atoi(fields[2][2 : len(fields[2])-1])
			num2, _ := strconv.Atoi(fields[3][2:])

			curr.buttonA = [2]int{num1, num2}

		case 1:
			num1, _ := strconv.Atoi(fields[2][2 : len(fields[2])-1])
			num2, _ := strconv.Atoi(fields[3][2:])

			curr.buttonB = [2]int{num1, num2}

		case 2:
			num1, _ := strconv.Atoi(fields[1][2 : len(fields[1])-1])
			num2, _ := strconv.Atoi(fields[2][2:])

			curr.Prize = [2]int{num1, num2}

		case 3:
			data = append(data, curr)
		}
	}

	data = append(data, curr)
}

func main() {
	parse(os.Stdin)

	P1 := 0
	for _, c := range data {
		P1 += c.tokens(3, 1)
	}

	P2 := 0
	for _, c := range data {
		P2 += c.correct(10000000000000).tokens(3, 1)
	}

	fmt.Printf("P1: %d\n", P1)
	fmt.Printf("P2: %d\n", P2)
}
