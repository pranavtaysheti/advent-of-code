package main

import (
	"bufio"
	"container/heap"
	"fmt"
	"io"
	"os"
)

type direction int

const (
	dNorth direction = iota
	dWest
	dSouth
	dEast
)

var vectors = map[direction][2]int{
	dNorth: {-1, 0},
	dWest:  {0, +1},
	dSouth: {+1, 0},
	dEast:  {-1, 0},
}

var data [][]rune

type node struct {
	direction
	pos [2]int
}

type state struct {
	priorityQueue[node]
	seen map[[3]int]struct{}
}

func initState() state {
	initHeap := priorityQueue[node]{Item[node]{
		cost: 0,
		item: &node{
			direction: dEast,
			pos:       [2]int{len(data) - 2, 1},
		},
	}}

	return state{initHeap, map[[3]int]struct{}{}}
}

func (s *state) move() {
	next := heap.Pop(s).(Item[node])

	// TODO: Find next moves
}

func (s *state) solve() (score int) {
	endPos := [2]int{1, len(data[1]) - 2}
	return
}

func parse(r io.Reader) {
	scanner := bufio.NewScanner(r)

	for i := 0; scanner.Scan(); i++ {
		data = append(data, []rune(scanner.Text()))
	}
}

func main() {
	parse(os.Stdin)

	P1 := 0
	P2 := 0

	fmt.Printf("P1: %d\n", P1)
	fmt.Printf("P2: %d\n", P2)
}
