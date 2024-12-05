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

func (u update) correctMiddle() int {
	numPosMap := map[int]int{}
	for i, n := range u {
		if _, ok := numPosMap[n]; !ok {
			numPosMap[n] = i
		}
	}

	corrected := slices.Clone(u)
	for i, n := range corrected[:(len(corrected)+1)/2] {
	swap:
		maxPos := i
		
		if beforeSlice, ok := orderRules[n]; ok {
			for _, b := range beforeSlice {
				if pos, ok := numPosMap[b]; ok {
					maxPos = max(maxPos, pos)
				}
			}

			if maxPos > i {
				numPosMap[corrected[i]], numPosMap[corrected[maxPos]] = numPosMap[corrected[maxPos]], numPosMap[corrected[i]]
				corrected[i], corrected[maxPos] = corrected[maxPos], corrected[i]
				n = corrected[i]
				goto swap
			}
		}
	}

	return corrected[(len(corrected)-1)/2]
}

var orderRules = map[int][]int{}
var updates = []update{}

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

	var P1 int
	var P2 int

	incorrectIndexes := []int{}

	for i, u := range updates {
		if u.check() {
			P1 += u[(len(u)-1)/2]
		} else {
			incorrectIndexes = append(incorrectIndexes, i)
		}
	}

	for _, i := range incorrectIndexes {
		P2 += updates[i].correctMiddle()
	}

	fmt.Printf("P1: %d\n", P1)
	fmt.Printf("P2: %d\n", P2)
}
