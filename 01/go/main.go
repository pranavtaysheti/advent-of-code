package main

import (
	"bufio"
	"fmt"
	"io"
	"log"
	"os"
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

func extractDigits(l string) (r []int) {
	for _, c := range l {
		if int(c) >= int('0') && int(c) <= int('9') {
			r = append(r, int(c)-int('0'))
		}
	}

	return
}

func decodeDigits(d []int) int {
	if len(d) == 0 {
		return 0
	}

	return 10*d[0] + d[len(d)-1]
}

func sumNumbers() (r int) {
	for _, l := range data {
		r += decodeDigits(extractDigits(l))
	}

	return
}
func main() {
	parseInput(os.Stdin)

	P1 := sumNumbers()
	P2 := 0

	fmt.Printf("P1: %d \n", P1)
	fmt.Printf("P2: %d \n", P2)
}
