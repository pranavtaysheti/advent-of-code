package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"strconv"
	"strings"
)

type update []int

func (u update) check() bool {
	numPosMap := map[int]int{}
	for i, n := range u {
		if _, ok := numPosMap[n]; !ok {
			numPosMap[n] = i
		}
	}

	for i, n := range u {
		if beforeSlice, ok := orderRules[n]; ok {
			for _, b := range beforeSlice {
				if pos, ok := numPosMap[b]; ok {
					if pos > i {
						return false
					}
				}
			}
		}
	}

	return true
}

func (u update) score() int {
	if u.check() {
		return u[(len(u)-1)/2]
	}

	return 0
}

var orderRules = map[int][]int{}
var updates = []update{}

func solve() (sum int) {
	for _, u := range updates {
		sum += u.score()
	}

	return
}

func parse(r io.Reader) {
	scanner := bufio.NewScanner(r)

	for scanner.Scan() {
		if len(scanner.Text()) == 0 {
			break
		}

		numStrSlice := strings.Split(scanner.Text(), "|")
		num1, _ := strconv.Atoi(numStrSlice[0])
		num2, _ := strconv.Atoi(numStrSlice[1])

		orderRules[num2] = append(orderRules[num2], num1)
	}

	for scanner.Scan() {
		numsStrSlice := strings.Split(scanner.Text(), ",")

		nums := []int{}
		for _, numStr := range numsStrSlice {
			n, _ := strconv.Atoi(numStr)
			nums = append(nums, n)
		}

		updates = append(updates, update(nums))
	}
}

func main() {
	parse(os.Stdin)
	
	P1 := solve()
	P2 := 0

	fmt.Printf("P1: %d\n", P1)
	fmt.Printf("P2: %d\n", P2)
}
