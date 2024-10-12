package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"strconv"
	"strings"
)

type rule interface {
	resolveAction() (redirection string, result bool)
}

type action string

func (a action) resolveAction() (redirection string, result bool) {
	switch a {
	case "A":
		return redirection, true
	case "R":
		return redirection, false
	default:
		return string(a), result
	}
}

type condition struct {
	category rune
	operator rune
	limit    int
}

func (c condition) test(p part) bool {
	switch c.operator {
	case '>':
		return p[c.category] > c.limit
	case '<':
		return p[c.category] < c.limit
	default:
		panic("unrecognized operator in condition argument")
	}

}

func (c condition) filter(p partRange) partRange {
	res := p

	switch c.operator {
	case '>':
		res[c.category] = categoryRange{
			low:  max(c.limit+1, res[c.category].low),
			high: res[c.category].high,
		}

	case '<':
		res[c.category] = categoryRange{
			low:  res[c.category].low,
			high: min(c.limit-1, res[c.category].high),
		}
	}

	return res
}

type conditionRule struct {
	condition
	action
}

type part map[rune]int

func (p part) score() (res int) {
	for _, amount := range p {
		res += amount
	}

	return
}

func (p part) solve(wf workflow) bool {
	for _, rule := range wf {
		switch v := rule.(type) {
		case conditionRule:
			if !v.test(p) {
				continue
			}
		}

		redirection, result := rule.resolveAction()
		if redirection == "" {
			return result
		}

		return p.solve(workflows[redirection])
	}

	panic(fmt.Sprintf("Unresolvable workflow: %v", wf))
}

type categoryRange struct {
	low  int
	high int
}

type partRange map[rune]categoryRange

func (p1 partRange) union(p2 partRange) partRange {
	res := partRange{}
	for r := range p1 {
		res[r] = categoryRange{
			low:  min(p1[r].low, p2[r].low),
			high: min(p1[r].high, p2[r].high),
		}
	}

	return res
}

func (p partRange) combinations() int {
	res := 1
	for _, cr := range p {
		res *= cr.high - cr.low + 1
	}

	return res
}

func makePartRange(c string, u int) partRange {
	res := partRange{}
	for _, r := range c {
		res[r] = categoryRange{1, u}
	}

	return res
}

type workflow []rule

var workflows = map[string]workflow{}
var parts = []part{}

func parseInput(r io.Reader) {
	scanner := bufio.NewScanner(r)

	parseCondition := func(c string) condition {
		limit, _ := strconv.Atoi(c[2:])
		return condition{rune(c[0]), rune(c[1]), limit}
	}

	for scanner.Scan() {
		if len(scanner.Text()) == 0 {
			break
		}

		line := scanner.Text()[:len(scanner.Text())-1]

		fields := strings.Split(line, "{")
		name := fields[0]
		rules := strings.Split(fields[1], ",")

		wf := workflow{}
		for _, r := range rules {
			ruleSplit := strings.Split(r, ":")
			switch len(ruleSplit) {
			case 1:
				wf = append(wf, action(ruleSplit[0]))
			case 2:
				wf = append(wf, conditionRule{parseCondition(ruleSplit[0]), action(ruleSplit[1])})
			}
		}

		workflows[name] = wf
	}

	for scanner.Scan() {
		line := scanner.Text()[1 : len(scanner.Text())-1]

		newPart := part{}
		partSplit := strings.Split(line, ",")
		for _, c := range partSplit {
			amount, _ := strconv.Atoi(c[2:])
			newPart[rune(c[0])] = amount
		}

		parts = append(parts, newPart)
	}
}

func solve() (res int) {
	for _, part := range parts {
		if part.solve(workflows["in"]) {
			res += part.score()
		}
	}

	return
}

func filter() (res int) {
	return res
}

func main() {
	parseInput(os.Stdin)
	P1 := solve()
	P2 := 0

	fmt.Printf("P1: %d \n", P1)
	fmt.Printf("P2: %d \n", P2)
}
