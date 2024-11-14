package main

import (
	"fmt"
	"io"
	"os"
)

var data string

func solve(s string, numChars int) int {
	buf := make([]rune, 0, len(s))

outer:
	for i, c := range s {
		buf = append(buf, c)
		if len(buf) == numChars+1 {
			buf = buf[1:]
		} else {
			continue
		}

		keys := map[rune]struct{}{}
		for _, d := range buf {
			if _, ok := keys[d]; ok {
				continue outer
			}

			keys[d] = struct{}{}
		}

		return i+1
	}

	panic("no marker found in text")

}
func main() {
	buf, _ := io.ReadAll(os.Stdin)
	data = string(buf)

	fmt.Printf("P1: %d\n", solve(data, 4))
	fmt.Printf("P2: %d\n", solve(data, 14))
}
