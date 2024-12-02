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

type report []int

func (r report) isSafe() bool {
	const max_diff = 3
	const min_diff = 1

	pattern := 0
	prevLevel := r[0]
	for _, level := range r[1:] {
		switch pattern {
		case 1:
			if level-prevLevel < min_diff || level-prevLevel > max_diff {
				return false
			}

		case -1:
			if prevLevel-level < min_diff || prevLevel-level > max_diff {
				return false
			}

		case 0:
			switch v := level - prevLevel; {
			case v <= -min_diff && v >= -max_diff:
				pattern = -1
			case v >= min_diff && v <= max_diff:
				pattern = +1
			default:
				return false
			}

		}

		prevLevel = level
	}

	return true
}

func (r report) dampen() bool {
	for i := range len(r) {
		newReport := report(slices.Concat(r[:i], r[i+1:]))
		if newReport.isSafe() {
			return true
		}
	}

	return false
}

var data []report

func countSafe() (safe int, dampenedSafe int) {
	for _, report := range data {
		if report.isSafe() {
			safe++
		} else {
			if report.dampen() {
				dampenedSafe++
			}
		}
	}

	return
}


func parse(r io.Reader) {
	scanner := bufio.NewScanner(r)

	for scanner.Scan() {
		levels := strings.Fields(scanner.Text())

		report := report(make([]int, len(levels)))
		for i, level := range levels {
			report[i], _ = strconv.Atoi(level)
		}

		data = append(data, report)
	}
}

func main() {
	parse(os.Stdin)
	
	safe, dampenedSafe := countSafe()
	P1 := safe
	P2 := safe + dampenedSafe

	fmt.Printf("P1: %d\n", P1)
	fmt.Printf("P2: %d\n", P2)
}
