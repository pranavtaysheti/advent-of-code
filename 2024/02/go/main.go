package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"strconv"
	"strings"
)

type report []int

func (r report) isSafe() bool {
	const max_diff = 3
	const min_diff = 1

	pattern := 0
	prev_level := r[0]
	for _, level := range r[1:] {
		switch pattern {
		case 1:
			if level-prev_level < min_diff || level-prev_level > max_diff {
				return false
			}

		case -1:
			if prev_level-level < min_diff || prev_level-level > max_diff {
				return false
			}

		case 0:
			switch v := level - prev_level; {
			case v <= -min_diff && v >= -max_diff:
				pattern = -1
			case v >= min_diff && v <= max_diff:
				pattern = +1
			default:
				return false
			}

		}

		prev_level = level
	}

	return true
}

var data []report

func countSafe() (count int) {
	for _, report := range data {
		if report.isSafe() {
			count++
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

	P1 := countSafe()
	P2 := 0

	fmt.Printf("P1: %d\n", P1)
	fmt.Printf("P2: %d\n", P2)

}
