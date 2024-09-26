package main

import (
	"bufio"
	"fmt"
	"io"
	"iter"
	"os"
	"strconv"
	"strings"
)

type direction rune

const (
	dRight direction = 'R'
	dDown            = 'D'
	dLeft            = 'L'
	dUp              = 'U'
)

type position struct {
	row int
	col int
}

type trench struct {
	pos    position
	colour int
}

type digPlan struct {
	cursor    position
	border    []trench
	perimeter int
}

var data = digPlan{
	border: []trench{},
}

func parseInput(r io.Reader) {
	parseLine := func(d direction, s int, c int) {
		currRow := data.cursor.row
		currCol := data.cursor.col

		switch d {
		case dRight:
			data.cursor = position{currRow, currCol + s}
		case dDown:
			data.cursor = position{currRow + s, currCol}
		case dLeft:
			data.cursor = position{currRow, currCol - s}
		case dUp:
			data.cursor = position{currRow - s, currCol}
		}

		data.border = append(data.border, trench{data.cursor, c})
		data.perimeter += s
	}

	scanner := bufio.NewScanner(r)
	for scanner.Scan() {
		fields := strings.Fields(scanner.Text())
		direction := direction(fields[0][0])
		length, _ := strconv.Atoi(fields[1])
		colour, _ := strconv.ParseInt(fields[2][2:len(fields[2])-1], 16, 0)

		parseLine(direction, length, int(colour))
	}
}

func pairWise[T any](s []T) iter.Seq2[T, T] {
	return func(yield func(T, T) bool) {
		for i := range len(s) - 1 {
			if !yield(s[i], s[i+1]) {
				return
			}
		}

		yield(s[len(s)-1], s[0])
	}
}

// Using https://en.wikipedia.org/wiki/Shoelace_formula
func (d digPlan) area() int {
	areaDoubled := 0
	for p1, p2 := range pairWise(data.border) {
		areaDoubled += p1.pos.col*p2.pos.row - p1.pos.row*p2.pos.col
	}

	return (areaDoubled + 2 + d.perimeter) / 2
}
func main() {
	parseInput(os.Stdin)

	P1 := data.area()
	P2 := 0

	fmt.Printf("P1: %d \n", P1)
	fmt.Printf("P2: %d \n", P2)
}
