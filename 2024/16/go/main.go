package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
)

var data [][]rune

func solve() (score int) {
	//TODO
	return
}

func parse(r io.Reader) {
	scanner := bufio.NewScanner(r)

	for scanner.Scan() {
		data = append(data, []rune(scanner.Text()))
	}
}

func main() {
	parse(os.Stdin)

	P1 := 0
	P2 := 0

	fmt.Printf("P1: %d\n", P1)
	fmt.Printf("P2: %d\n", P2)
}
