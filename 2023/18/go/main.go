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
type parser func(l string) (direction, int)

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
	border    []position
	perimeter int
}

var p1data = digPlan{
	border: []position{},
}

var p2data = digPlan{
	border: []position{},
}

func p1parser(l string) (direction, int) {
	fields := strings.Fields(l)
	direction := direction(fields[0][0])
	length, _ := strconv.Atoi(fields[1])

	return direction, length
}

func p2parser(l string) (direction, int) {
	fields := strings.Fields(l)
	colourField := fields[2]
	directionInt, _ := strconv.Atoi(colourField[len(colourField)-2 : len(colourField)-1])
	var direction direction
	switch directionInt {
	case 0:
		direction = 'R'
	case 1:
		direction = 'D'
	case 2:
		direction = 'L'
	case 3:
		direction = 'U'
	}

	length, _ := strconv.ParseInt(colourField[2:len(colourField)-2], 16, 0)

	return direction, int(length)
}

func parseInput(r io.Reader, p []*digPlan, e []parser) {
	parseLine := func(p *digPlan, d direction, s int) {
		currRow := p.cursor.row
		currCol := p.cursor.col

		switch d {
		case dRight:
			p.cursor = position{currRow, currCol + s}
		case dDown:
			p.cursor = position{currRow + s, currCol}
		case dLeft:
			p.cursor = position{currRow, currCol - s}
		case dUp:
			p.cursor = position{currRow - s, currCol}
		}

		p.border = append(p.border, p.cursor)
		p.perimeter += s
	}

	scanner := bufio.NewScanner(r)
	for scanner.Scan() {
		for i := range len(p) {
			direction, length := e[i](scanner.Text())
			parseLine(p[i], direction, length)
		}
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

// Using https://en.wikipedia.org/wiki/Shoelace_formula, https://en.wikipedia.org/wiki/Pick's_theorem
func (d digPlan) area() int {
	areaDoubled := 0
	for p1, p2 := range pairWise(d.border) {
		areaDoubled += p1.col*p2.row - p1.row*p2.col
	}

	return (areaDoubled + 2 + d.perimeter) / 2
}

func main() {
	parseInput(os.Stdin, []*digPlan{&p1data, &p2data}, []parser{p1parser, p2parser})

	P1 := p1data.area()
	P2 := p2data.area()

	fmt.Printf("P1: %d \n", P1)
	fmt.Printf("P2: %d \n", P2)
}
