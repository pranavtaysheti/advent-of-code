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

var data []card

func parseData(r io.Reader) {
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

		data = append(data, card{
			winning: winning,
			have:    have,
		})
	}
}

func calculateScore(c card) int {
	r := 0.5

	for _, n := range c.have {
		if _, ok := c.winning[n]; ok {
			r *= 2
		}
	}

	return int(math.Floor(r))
}

func sumScore() (r int) {
	for _, c := range data {
		r += calculateScore(c)
	}

	return
}

func main() {
	parseData(os.Stdin)

	P1 := sumScore()
	P2 := 0

	fmt.Printf("P1: %d \n", P1)
	fmt.Printf("P2: %d \n", P2)
}
