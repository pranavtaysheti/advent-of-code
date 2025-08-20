package main

import (
	"bufio"
	"fmt"
	"io"
	"iter"
	"math"
	"os"
	"slices"
	"strconv"
	"strings"
)

type keypadType int

const (
	ktDoor keypadType = iota
	ktRobot
)

type keypad struct {
	layout [4][3]rune
	start  pos
}

func (k keypad) getPos(e rune) pos {
	for i, row := range k.layout {
		for j, c := range row {
			if c == e {
				return pos{i, j}
			}
		}
	}

	return pos{-1, -1}
}

func (k keypad) simulate(p pos, c command) bool {
	symVec := map[rune]pos{
		'>': {0, 1},
		'v': {+1, 0},
		'^': {-1, 0},
		'<': {0, -1},
	}

	curr := p
	for _, r := range c {
		curr = curr.add(symVec[r])
		c_row, c_col := curr.split()
		if k.layout[c_row][c_col] == ' ' {
			return false
		}
	}

	return true
}

var doorKeypad = keypad{[4][3]rune{
	{'7', '8', '9'},
	{'4', '5', '6'},
	{'1', '2', '3'},
	{' ', '0', 'A'},
}, pos{3, 2}}

var robotKeypad = keypad{[4][3]rune{
	{' ', '^', 'A'},
	{'<', 'v', '>'},
}, pos{0, 2}}

// generated using generate/expansions.py
var expansionMap = map[string]map[string]int{
	"":    {"": 1},
	"<":   {">>^": 1, "v<<": 1},
	"<<":  {"": 1, ">>^": 1, "v<<": 1},
	"<<^": {"": 1, ">": 1, ">^": 1, "v<<": 1},
	"<<v": {"": 1, ">": 1, "^>": 1, "v<<": 1},
	"<^":  {">": 1, ">^": 1, "v<<": 1},
	"<v":  {">": 1, "^>": 1, "v<<": 1},
	">":   {"^": 1, "v": 1},
	">>":  {"": 1, "^": 1, "v": 1},
	">>^": {"": 1, "<^": 1, ">": 1, "v": 1},
	">>v": {"": 1, "<": 1, "^>": 1, "v": 1},
	">^":  {"<^": 1, ">": 1, "v": 1},
	">v":  {"<": 1, "^>": 1, "v": 1},
	"^":   {"<": 1, ">": 1},
	"^<":  {"<": 1, ">>^": 1, "v<": 1},
	"^<<": {"": 1, "<": 1, ">>^": 1, "v<": 1},
	"^>":  {"<": 1, "^": 1, "v>": 1},
	"^>>": {"": 1, "<": 1, "^": 1, "v>": 1},
	"v":   {"<v": 1, "^>": 1},
	"v<":  {"<": 1, "<v": 1, ">>^": 1},
	"v<<": {"": 1, "<": 1, "<v": 1, ">>^": 1},
	"v>":  {"<v": 1, ">": 1, "^": 1},
	"v>>": {"": 1, "<v": 1, ">": 1, "^": 1},
}

func repeat[E any](e E, n int) iter.Seq[E] {
	return func(yield func(E) bool) {
		for range n {
			if !yield(e) {
				break
			}
		}
	}
}

type pos [2]int

func (p pos) split() (r int, c int) {
	return p[0], p[1]
}

func (start pos) path(end pos) pos {
	e_row, e_col := end.split()
	s_row, s_col := start.split()

	return pos{e_row - s_row, e_col - s_col}
}

func (p pos) add(d pos) pos {
	c_row, c_col := p.split()
	d_row, d_col := d.split()

	return pos{c_row + d_row, c_col + d_col}
}

type command string

type parsedCommand map[string]int

func expand(p parsedCommand) parsedCommand {
	res := parsedCommand{}
	for exp, qty := range p {
		for exp_2, qty_2 := range expansionMap[exp] {
			if _, ok := res[exp_2]; !ok {
				res[exp_2] = qty * qty_2
			} else {
				res[exp_2] += qty * qty_2
			}
		}
	}

	return res
}

func (p parsedCommand) cost() (res int) {
	for exp, qty := range p {
		res += (len(exp)*qty + qty)
	}

	return
}

func (c command) parse() parsedCommand {
	res := parsedCommand{}
	parts := strings.Split(string(c), "A")
	for _, p := range parts[:len(parts)-1] {
		if _, ok := res[p]; !ok {
			res[p] = 1
		} else {
			res[p]++
		}
	}

	return res
}

type robot struct {
	curr     pos
	password string
	keypad
}

func makeRobot(kt keypadType, p string) robot {
	var keypad keypad
	switch kt {
	case ktDoor:
		keypad = doorKeypad
	case ktRobot:
		keypad = robotKeypad
	}

	return robot{
		curr:     keypad.start,
		password: p,
		keypad:   keypad,
	}
}

func (r *robot) buildCommand() map[command]struct{} {
	prev_res := map[command]struct{}{"": {}}
	res := map[command]struct{}{}
	for _, e := range r.password {
		e_pos := r.keypad.getPos(e)
		d_row, d_col := r.curr.path(e_pos).split()
		d_row_abs, d_col_abs := max(d_row, -d_row), max(d_col, -d_col)

		part_ver := make([]rune, 0, 3)
		part_hor := make([]rune, 0, 2)
		if d_row > 0 {
			part_ver = slices.AppendSeq(part_ver, repeat('v', d_row_abs))
		}
		if d_row < 0 {
			part_ver = slices.AppendSeq(part_ver, repeat('^', d_row_abs))
		}
		if d_col > 0 {
			part_hor = slices.AppendSeq(part_hor, repeat('>', d_col_abs))
		}
		if d_col < 0 {
			part_hor = slices.AppendSeq(part_hor, repeat('<', d_col_abs))
		}

		for c := range prev_res {
			vh := command(append(slices.Concat(part_ver, part_hor), 'A'))
			hv := command(append(slices.Concat(part_hor, part_ver), 'A'))

			if r.keypad.simulate(r.curr, vh) {
				res[c+vh] = struct{}{}
			}

			if r.keypad.simulate(r.curr, hv) {
				res[c+hv] = struct{}{}
			}
		}

		r.curr = e_pos
		prev_res = res
		res = map[command]struct{}{}
	}

	return prev_res
}

func solve(p string, layers int) int {
	r := makeRobot(ktDoor, p)
	c_comm := map[command]struct{}{}
	for c := range r.buildCommand() {
		r = makeRobot(ktRobot, string(c))
		for c2 := range r.buildCommand() {
			c_comm[c2] = struct{}{}
		}
	}

	min_cost := math.MaxInt
	for c := range c_comm {
		c_exp := c.parse()
		for range layers - 2 {
			c_exp = expand(c_exp)
		}

		cost := c_exp.cost()
		if cost < min_cost {
			min_cost = cost
		}
	}

	return min_cost
}

var data = []string{}

func parse(r io.Reader) {
	scanner := bufio.NewScanner(r)
	for scanner.Scan() {
		data = append(data, scanner.Text())
	}
}

func main() {
	parse(os.Stdin)

	P1 := 0
	for _, p := range data {
		num, _ := strconv.Atoi(p[:len(p)-1])
		P1 += num * solve(p, 3)
	}

	fmt.Printf("P1: %d\n", P1)

	P2 := 0
	for _, p := range data {
		num, _ := strconv.Atoi(p[:len(p)-1])
		P2 += num * solve(p, 26)
	}

	fmt.Printf("P2: %d\n", P2)
}
