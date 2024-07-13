package main

import (
	"bufio"
	"fmt"
	"io"
	"log"
	"os"
	"strings"
)

var numberStrings = []string{
	"zero",
	"one",
	"two",
	"three",
	"four",
	"five",
	"six",
	"seven",
	"eight",
	"nine",
}

var data []string = make([]string, 0, 1000)

func parseInput(r io.Reader) {
	scanner := bufio.NewScanner(r)
	for i := 1; scanner.Scan(); i++ {
		if scanner.Err() != nil {
			log.Fatal(scanner.Err())
		}
		data = append(data, scanner.Text())
	}
}

func extractNumbers(l string, countSpelled bool) (r []int) {
	getDigit := func(c rune) bool {
		if int(c) >= int('0') && int(c) <= int('9') {
			r = append(r, int(c)-int('0'))
			return true
		}

		return false
	}

	getSpelled := func(s string) bool {
		for i, sub := range numberStrings {
			if strings.Contains(s[max(0, len(s)-len(sub)):], sub) {
				r = append(r, i)
				return true
			}

		}

		return false
	}

	for i, c := range l {
		if getDigit(c) {
			continue
		}

		if countSpelled {
			getSpelled(l[max(0, i-4) : i+1])
		}
	}

	return
}

func sumNumbers(countSpelled bool) (r int) {
	decodeDigits := func(d []int) int {
		if len(d) == 0 {
			return 0
		}

		return 10*d[0] + d[len(d)-1]
	}

	for _, l := range data {
		r += decodeDigits(extractNumbers(l, countSpelled))
	}

	return
}
func main() {
	parseInput(os.Stdin)

	P1 := sumNumbers(false)
	P2 := sumNumbers(true)

	fmt.Printf("P1: %d \n", P1)
	fmt.Printf("P2: %d \n", P2)
}
