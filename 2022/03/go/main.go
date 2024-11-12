package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"strings"
)

type item rune

func (i item) priority() int {
	if int(i) >= 97 && int(i) <= 122 {
		return int(i) - 96
	}

	if int(i) >= 65 && int(i) <= 90 {
		return int(i) - 64 + 26
	}

	panic("this rune should not be in input")
}

type rugsack []item

func (rs rugsack) div() int {
	return len(rs)/2
}

func (rs rugsack) commonItem() item {
	for _, c := range rs[:rs.div()] {
		if strings.ContainsRune(string(rs[rs.div():]), rune(c)) {
			return item(c)
		}
	}

	panic("no common rune found")
}

type group [3]rugsack 


var data []rugsack

func parse(r io.Reader) {
	scanner := bufio.NewScanner(r)

	for scanner.Scan() {
		line := scanner.Text()
		rs := rugsack(line)
		data = append(data, rs)
	}
}

func solve() (res int) {
	for _, rs := range data {
		res += rs.commonItem().priority()
	}

	return
}

func main() {
	parse(os.Stdin)

	P1 := solve()
	P2 := 0

	fmt.Printf("P1: %d \n", P1)
	fmt.Printf("P2: %d \n", P2)
}
