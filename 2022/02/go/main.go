package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"strings"
)

type shape int

const (
	Rock shape = 1 + iota
	Paper
	Scissor
)

type round struct {
	col1 rune
	col2 rune
}

func (r round) score() int {
	return score(shape(r.col1-64), shape(r.col2-87))
}

func (r round) choose() int {
	opp := shape(r.col1 - 64)

	var me shape
	switch r.col2 {
	case 'X': // Losing
		if opp == Rock {
			me = Scissor
		} else {
			me = opp - 1
		}

	case 'Y': //Draw
		me = opp

	case 'Z': // Winning
		if opp == Scissor {
			me = Rock
		} else {
			me = opp + 1
		}
	}

	return score(opp, me)
}

type game []round

func (g game) score() (res int) {
	for _, round := range g {
		res += round.score()
	}

	return
}

func (g game) choose() (res int) {
	for _, round := range g {
		res += round.choose()
	}

	return
}

var data game

func score(opp shape, me shape) int {
	res := int(me) - int(opp)
	if res == +2 || res == -1 { //losing
		res = 0
	} else if res == +1 || res == -2 { //winning
		res = 2
	} else if res == 0 { //draw
		res = 1
	}

	res = 3*res + int(me)
	return res

}
func parseInput(r io.Reader) {
	scanner := bufio.NewScanner(r)

	for scanner.Scan() {
		fields := strings.Fields(scanner.Text())
		p1 := rune(fields[0][0])
		p2 := rune(fields[1][0])

		data = append(data, round{p1, p2})
	}
}

func main() {
	parseInput(os.Stdin)

	P1 := data.score()
	P2 := data.choose()

	fmt.Printf("P1: %d \n", P1)
	fmt.Printf("P2: %d \n", P2)
}
