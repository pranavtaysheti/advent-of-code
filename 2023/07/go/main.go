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
	"strings"
)

type handBidType int

var strength = []rune{'2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A'}
var jokerStrength = []rune{'J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A'}

type handBid struct {
	hand string
	bid  int
}

type handBidScore struct {
	typeScore int
	score     int
	bid       int
}

var data = []handBid{}

func count(h string) map[rune]int {
	count := map[rune]int{}
	for _, c := range h {
		count[c]++
	}

	return count
}

func score(h string, m []rune) (res int) {
	for _, c := range h {
		res *= len(m)
		res += slices.Index(m, c)
	}

	return
}

func typeScore(h string) (res int) {
	for v := range maps.Values(count(h)) {
		res += int(math.Pow(float64(v), 2))
	}

	return
}

func substituteJoker(h string) string {
	count := count(h)
	var currMax rune
	currMaxqty := 0

	for k, v := range maps.All(count) {
		if k == 'J' {
			continue
		}

		if v > currMaxqty {
			currMax = k
			currMaxqty = v
		}
	}

	if currMaxqty == 0 {
		return h
	}

	return strings.Replace(h, "J", string(currMax), -1)
}

func scoreAll(f func(h handBid) handBidScore) (res []handBidScore) {
	for _, h := range data {
		res = append(res, f(h))
	}

	return
}

func scoreHandBid(h handBid) handBidScore {
	return handBidScore{
		typeScore(h.hand),
		score(h.hand, strength),
		h.bid,
	}
}

func jokerScoreHandBid(h handBid) handBidScore {
	return handBidScore{
		typeScore(substituteJoker(h.hand)),
		score(h.hand, jokerStrength),
		h.bid,
	}
}

func sortInput(d []handBidScore) []handBidScore {
	slice := slices.Clone(d)
	sortFunc := func(a, b handBidScore) int {
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

func totalWinning(d []handBidScore) (res int) {
	for i, s := range d {
		res += (i + 1) * s.bid
	}

	return
}

func main() {
	data = parseInput(os.Stdin)

	P1 := totalWinning(sortInput(scoreAll(scoreHandBid)))
	P2 := totalWinning(sortInput(scoreAll(jokerScoreHandBid)))

	fmt.Printf("P1: %d \n", P1)
	fmt.Printf("P2: %d \n", P2)
}
