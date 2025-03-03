package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"strings"
)

func count[T any](s []T, fn func(e T) bool) (count int) {
	for _, e := range s {
		if fn(e) {
			count++
		}
	}

	return count
}

func sum[T any](s []T, fn func(e T) int) (sum int) {
	for _, e := range s {
		sum += fn(e)
	}

	return
}

type towels []string

func (t towels) check(p string) bool {
	tabulation := make([]bool, len(p)+1)
	tabulation[0] = true

	for i := range len(p) + 1 {
		if !tabulation[i] {
			continue
		}

		for _, w := range t {
			if i+len(w) <= len(p) {
				if w == p[i:i+len(w)] {
					tabulation[i+len(w)] = true
				}
			}
		}
	}

	return tabulation[len(p)]
}

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

	P1 := count(patterns, towels.check)
	P2 := sum(patterns, towels.count)

	fmt.Printf("P1: %d\n", P1)
	fmt.Printf("P2: %d\n", P2)
}
