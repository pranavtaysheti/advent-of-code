package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"strings"
)

type warehouse struct {
	instructions []rune
	floor        [][]rune
	cursor       [2]int
}

var data = warehouse{}

func parse(r io.Reader) {
	scanner := bufio.NewScanner(r)

	for i := 0; scanner.Scan(); i++ {
		if len(scanner.Text()) == 0 {
			break
		}

		line := []rune(scanner.Text())
		if j := strings.IndexRune(scanner.Text(), '@'); j >= 0 {
			data.cursor = [2]int{i, j}
			line[j] = '.'
		}

		data.floor = append(data.floor, line)
	}

	for scanner.Scan() {
		data.instructions = append(data.instructions, []rune(scanner.Text())...)
	}
}

func main() {
	parse(os.Stdin)

	P1 := 0
	P2 := 0

	fmt.Printf("P1: %d\n", P1)
	fmt.Printf("P2: %d\n", P2)
}
