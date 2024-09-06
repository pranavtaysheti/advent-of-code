package main

import (
	"bufio"
	"errors"
	"fmt"
	"io"
	"os"
)

const width int = 140

type symbol struct {
	symbol  rune
	col     int
	numbers []int
}

type digit struct {
	digit int
	col   int
}

type number struct {
	digits []digit
	number int
}

var numberData = [][]number{}
var symbolData = [][]symbol{}

func (s *symbol) addNumber(n *number) {
	s.numbers = append(s.numbers, n.number)
}

func (n *number) addDigit(col int, c rune) error {
	if d := int(c) - 48; d >= 0 && d <= 9 {
		n.digits = append(n.digits, digit{
			digit: d,
			col:   col,
		})
		n.number = 10*n.number + d
		return nil
	}

	return errors.New("rune not a number")
}

func link(s *symbol, n *number) bool {
	for _, d := range n.digits {
		cols := []int{d.col}
		if d.col > 0 {
			cols = append(cols, d.col-1)
		}

		if d.col < width-1 {
			cols = append(cols, d.col+1)
		}

		for _, c := range cols {
			if c == s.col {
				s.numbers = append(s.numbers, n.number)
				return true
			}

		}
	}

	return false
}

func linkAll() {
	for i := 0; i < len(symbolData); i++ {
		number_rows := []int{i}
		if i > 0 {
			number_rows = append(number_rows, i-1)
		}
		if i < len(symbolData)-1 {
			number_rows = append(number_rows, i+1)
		}

		for s := range symbolData[i] {
			for _, l := range number_rows {
				for n := range numberData[l] {
					link(&symbolData[i][s], &numberData[l][n])
				}
			}
		}
	}
}

func parseInput(r io.Reader) {
	scanner := bufio.NewScanner(r)
	for i := 0; scanner.Scan(); i++ {
		line_symbols := []symbol{}
		line_numbers := []number{}

		currParseNumber := number{}
		for j, c := range scanner.Text() {
			if (int(c) >= 33 && int(c) <= 45) || int(c) == 47 || (int(c) >= 58 && int(c) <= 64) {
				line_symbols = append(line_symbols, symbol{
					symbol:  c,
					col:     j,
					numbers: []int{},
				})
			}

			if err := (&currParseNumber).addDigit(j, c); err != nil {
				if len(currParseNumber.digits) > 0 {
					line_numbers = append(line_numbers, currParseNumber)
					currParseNumber = number{}
				}
			}
		}

		if len(currParseNumber.digits) > 0 {
			line_numbers = append(line_numbers, currParseNumber)
		}

		numberData = append(numberData, line_numbers)
		symbolData = append(symbolData, line_symbols)
	}

	return
}

func sumPartNumbers() (r int) {
	for i := range symbolData {
		for j := range symbolData[i] {
			for _, n := range symbolData[i][j].numbers {
				r += n
			}
		}
	}

	return
}

func sumGearRatios() (r int) {
	for i := range symbolData {
		for j := range symbolData[i] {
			if symbolData[i][j].symbol != '*' {
				continue
			}

			numbers := symbolData[i][j].numbers

			if len(numbers) != 2 {
				continue
			}

			r += numbers[0] * numbers[1]

		}
	}

	return
}

func main() {
	parseInput(os.Stdin)
	linkAll()

	P1 := sumPartNumbers()
	P2 := sumGearRatios()

	fmt.Printf("P1: %d \n", P1)
	fmt.Printf("P2: %d \n", P2)
}
