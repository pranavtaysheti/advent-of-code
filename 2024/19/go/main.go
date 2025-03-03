package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"strings"
)

func count(nums []int) (count int) {
	for _, n := range nums {
		if n > 0 {
			count++
		}
	}

	return count
}

func sum(nums []int) (sum int) {
	for _, n := range nums {
		sum += n
	}

	return
}

type towels []string

func (t towels) count(p string) int {
	counts := make([]int, len(p)+1)
	counts[0] = 1

	for i := range len(p) + 1 {
		if counts[i] == 0 {
			continue
		}

		for _, w := range t {
			if i+len(w) <= len(p) {
				if w == p[i:i+len(w)] {
					counts[i+len(w)] += counts[i]
				}
			}
		}
	}

	return counts[len(p)]
}

func parse(r io.Reader) (towels towels, patterns []string) {
	scanner := bufio.NewScanner(r)

	scanner.Scan()
	towels = strings.Split(scanner.Text(), ", ")

	scanner.Scan()

	for scanner.Scan() {
		patterns = append(patterns, scanner.Text())
	}

	return
}

func main() {
	towels, patterns := parse(os.Stdin)

	counts := make([]int, len(patterns))
	for i, p := range patterns {
		counts[i] = towels.count(p)
	}

	P1 := count(counts)
	P2 := sum(counts)

	fmt.Printf("P1: %d\n", P1)
	fmt.Printf("P2: %d\n", P2)
}
