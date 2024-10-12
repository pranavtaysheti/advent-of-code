package main

import (
	"bufio"
	"fmt"
	"io"
	"math"
	"os"
	"strconv"
	"strings"
)

type card struct {
	winning map[int]struct{}
	have    []int
}

type matchedCard struct {
	card
	matches int
}

var data []matchedCard

func parseData(r io.Reader) (res []card) {
	strToIntSlice := func(s []string) (r []int) {
		for _, num := range s {
			v, _ := strconv.Atoi(num)
			r = append(r, v)
		}

		return
	}

	strToIntMap := func(s []string) map[int]struct{} {
		r := map[int]struct{}{}
		for _, num := range s {
			v, _ := strconv.Atoi(num)
			r[v] = struct{}{}
		}

		return r
	}

	scanner := bufio.NewScanner(r)
	for scanner.Scan() {
		cardText := scanner.Text()
		winning := strToIntMap(strings.Fields(cardText[9:39]))
		have := strToIntSlice(strings.Fields(cardText[41:]))

		res = append(res, card{
			winning: winning,
			have:    have,
		})
	}

	return
}

func compile(d []card) (res []matchedCard) {
	for _, c := range d {
		matches := 0
		for _, n := range c.have {
			if _, ok := c.winning[n]; ok {
				matches += 1
			}
		}

		res = append(res, matchedCard{c, matches})
	}

	return
}

func sumScore(d []matchedCard) (r int) {
	calculateScore := func(c matchedCard) int {
		return int(math.Floor(math.Pow(2, float64(c.matches-1))))
	}

	for _, c := range d {
		r += calculateScore(c)
	}

	return
}

func sumScratchcardsCopies(d []matchedCard) (res int) {
	copies := make([]int, len(data))
	for i := range copies {
		copies[i] = 1
	}

	for i, c := range d {
		for j := range c.matches {
			copies[i+j+1] += copies[i]
		}
	}

	for _, n := range copies {
		res += n
	}

	return
}

func main() {
	data = compile(parseData(os.Stdin))

	P1 := sumScore(data)
	P2 := sumScratchcardsCopies(data)

	fmt.Printf("P1: %d \n", P1)
	fmt.Printf("P2: %d \n", P2)
}
