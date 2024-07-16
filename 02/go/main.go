package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"strconv"
	"strings"
)

type cubes struct {
	green int
	red   int
	blue  int
}

type game []cubes

var data []game

const (
	maxRed   = 12
	maxGreen = 13
	maxBlue  = 14
)

func parseInput(r io.Reader) {
	parseGame := func(s string) (d game) {
		gameString := s[strings.IndexRune(s, ':')+2:]
		games := strings.Split(gameString, "; ")
		for _, g := range games {
			new_cubes := cubes{}
			colours := strings.Split(g, ", ")
			for _, c := range colours {
				hand := strings.Split(c, " ")
				qty, _ := strconv.Atoi(hand[0])
				colour := hand[1]

				switch colour {
				case "green":
					new_cubes.green = qty
					break
				case "red":
					new_cubes.red = qty
				case "blue":
					new_cubes.blue = qty
				}
			}

			d = append(d, new_cubes)
		}

		return
	}

	scanner := bufio.NewScanner(r)
	for i := 0; scanner.Scan(); i++ {
		data = append(data, parseGame(scanner.Text()))
	}
}

func totalPossibleSum() (r int) {
	isPossible := func(g game) bool {
		for _, c := range g {
			if c.red > maxRed || c.green > maxGreen || c.blue > maxBlue {
				return false
			}
		}

		return true
	}

	for i, g := range data {
		if isPossible(g) {
			r += i + 1
		}
	}

	return
}

func main() {
	parseInput(os.Stdin)

	P1 := totalPossibleSum()
	P2 := 0

	fmt.Printf("P1: %d \n", P1)
	fmt.Printf("P2: %d \n", P2)
}
