package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"slices"
	"strconv"
	"strings"
)

type crate rune

type stacks [][]crate

func (s stacks) moveCrateOne(i instruction) {
	for range i.quantity {
		s[i.to-1] = append(s[i.to-1], s[i.from-1][len(s[i.from-1])-1])
		s[i.from-1] = s[i.from-1][:len(s[i.from-1])-1]
	}
}

func (s stacks) moveCrateAll(i instruction) {
	s[i.to-1] = append(s[i.to-1], s[i.from-1][len(s[i.from-1])-i.quantity:]...)
	s[i.from-1] = s[i.from-1][:len(s[i.from-1])-i.quantity]
}

func (s stacks) top() string {
	res := []rune{}
	for _, stack := range s {
		res = append(res, rune(stack[len(stack)-1]))
	}

	return string(res)
}

func (s stacks) clone() stacks {
	res := make([][]crate, len(s))
	for i := range len(s) {
		res[i] = slices.Clone(s[i])
	}

	return res
}

type instruction struct {
	quantity int
	from     int
	to       int
}

var state = stacks(make([][]crate, 0))
var instructions = []instruction{}

func parse(r io.Reader) {
	scanner := bufio.NewScanner(r)

	for scanner.Scan() {
		if scanner.Text()[1] == '1' {
			break
		}

		if len(state) == 0 {
			for pos := 1; pos < len(scanner.Text()); pos += 4 {
				state = append(state, []crate{})
			}
		}

		line := scanner.Text()
		for pos, i := 1, 0; pos < len(line); pos += 4 {
			if c := line[pos]; c != ' ' {
				state[i] = append(state[i], crate(c))
			}

			i++
		}
	}

	capLen := 0
	for _, stack := range state {
		capLen = max(capLen, len(stack)*2)
	}

	for i, stack := range state {
		newStack := slices.Clone(stack)
		slices.Reverse(newStack)

		state[i] = make([]crate, 0, capLen)
		state[i] = append(state[i], newStack...)
	}

	scanner.Scan() //skip past blank line

	for scanner.Scan() {
		fields := strings.Fields(scanner.Text())

		nums := make([]int, 0, 3)
		for _, pos := range []int{1, 3, 5} {
			word := fields[pos]
			num, _ := strconv.Atoi(word)
			nums = append(nums, num)
		}

		instructions = append(instructions, instruction{nums[0], nums[1], nums[2]})
	}

}
func main() {
	parse(os.Stdin)

	p1State := state.clone()
	for _, i := range instructions {
		p1State.moveCrateOne(i)
	}

	p2State := state.clone()
	for _, i := range instructions {
		p2State.moveCrateAll(i)
	}

	P1 := p1State.top()
	P2 := p2State.top()

	fmt.Printf("P1: %s\n", P1)
	fmt.Printf("P2: %s\n", P2)
}
