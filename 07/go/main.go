package main

import (
	"bufio"
	"fmt"
	"io"
	"maps"
	"math"
	"os"
	"slices"
	"strconv"
)

type handBidType int

var strength = []rune{'2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A'}

type handBid struct {
	hand string
	bid  int
}

type scoredHandBid struct {
	handBid
	typeScore int
	score     int
}

var data = []scoredHandBid{}

func (h handBid) score() (res int) {
	for _, c := range h.hand {
		res *= 13
		res += slices.Index(strength, c)
	}

	return
}

func (h handBid) typeScore() (res int) {
	count := map[rune]int{}
	for _, c := range h.hand {
		count[c]++
	}

	for v := range maps.Values(count) {
		res += int(math.Pow(float64(v), 2))
	}

	return
}

func newScoredHandBid(h handBid) scoredHandBid {
	return scoredHandBid{
		h,
		h.typeScore(),
		h.score(),
	}
}

func sortInput(d []handBid) []scoredHandBid {
	slice := []scoredHandBid{}
	for _, h := range d {
		slice = append(slice, newScoredHandBid(h))
	}

	sortFunc := func(a, b scoredHandBid) int {
		if a.typeScore != b.typeScore {
			return a.typeScore - b.typeScore
		}

		return a.score - b.score
	}

	slices.SortFunc(slice, sortFunc)
	return slice
}

func parseInput(r io.Reader) (res []handBid) {
	scanner := bufio.NewScanner(r)
	for scanner.Scan() {
		line := scanner.Text()
		hand := line[:5]
		bid, _ := strconv.Atoi(line[6:])
		res = append(res, handBid{hand, bid})
	}

	return
}

func totalWinning() (res int) {
	for i, s := range data {
		res += (i + 1) * s.bid
	}

	return
}
func main() {
	data = sortInput(parseInput(os.Stdin))

	P1 := totalWinning()
	P2 := 0

	fmt.Printf("P1: %d \n", P1)
	fmt.Printf("P2: %d \n", P2)
}
