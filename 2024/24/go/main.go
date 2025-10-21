package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"strconv"
	"strings"
)

type wireState int

const (
	wsOff wireState = iota
	wsOn
	wsNone
)

type wire struct {
	name   string
	state  wireState
	input  *gate
	output []*gate
}

type gateSpec int

const (
	gsAND gateSpec = iota
	gsOR
	gsXOR
)

type gate struct {
	spec   gateSpec
	input  [2]*wire
	output *wire
}

type circuit struct {
	initState []*wire
	wires     map[*wire]struct{}
	zScore    int
}

func (c *circuit) update(w *wire) []*wire {
	res := []*wire{}

	for _, g := range w.output {
		calculatedInputs := 0
		for _, w := range g.input {
			if w.state != wsNone {
				calculatedInputs++
			}
		}

		if calculatedInputs != 2 {
			continue
		}

		switch g.spec {
		case gsAND:
			if g.input[0].state == wsOn && g.input[1].state == wsOn {
				g.output.state = wsOn
			}
		case gsOR:
			if g.input[0].state == wsOn || g.input[1].state == wsOn {
				g.output.state = wsOn
			}
		case gsXOR:
			if g.input[0].state+g.input[1].state == 1 {
				g.output.state = wsOn
			}
		}

		if g.output.state == wsNone {
			g.output.state = wsOff
		}

		res = append(res, g.output)
	}

	return res
}

func (c *circuit) solve() {
	curr := map[*wire]struct{}{}
	for _, wire := range c.initState {
		curr[wire] = struct{}{}
	}

	for {
		nextCurr := map[*wire]struct{}{}
		for w := range curr {
			if w.name[0] == 'z' {
				if w.state != wsOn {
					continue
				}

				num, _ := strconv.Atoi(string(w.name[1:]))
				data.zScore |= (1 << num)

				continue
			}

			for _, n := range c.update(w) {
				nextCurr[n] = struct{}{}
			}
		}

		curr = map[*wire]struct{}{}
		curr = nextCurr
		if len(curr) == 0 {
			break
		}
	}
}

var data = circuit{
	initState: []*wire{},
	wires:     map[*wire]struct{}{},
}

func parse(r io.Reader) {
	scanner := bufio.NewScanner(r)
	seenWires := map[string]*wire{}

	for scanner.Scan() {
		line := scanner.Text()
		if len(line) == 0 {
			break
		}

		vals := strings.Split(line, ": ")
		name := vals[0]
		state, _ := strconv.Atoi(vals[1])

		newWire := wire{
			name:  name,
			state: wireState(state),
		}

		data.initState = append(data.initState, &newWire)
		data.wires[&newWire] = struct{}{}
		seenWires[name] = &newWire
	}

	for scanner.Scan() {
		line := scanner.Text()
		words := strings.Split(line, " ")
		gateSpecStr := words[1]
		wireNames := []string{words[0], words[2], words[4]}

		var gs gateSpec
		switch gateSpecStr {
		case "AND":
			gs = gsAND
		case "OR":
			gs = gsOR
		case "XOR":
			gs = gsXOR
		}

		newGate := gate{
			spec: gs,
		}

		wires := make([]*wire, 3)
		for i, wn := range wireNames {
			if w, ok := seenWires[wn]; !ok {
				wires[i] = &wire{
					name:  wn,
					state: wsNone,
				}

				data.wires[wires[i]] = struct{}{}
				seenWires[wn] = wires[i]
			} else {
				wires[i] = w
			}
		}

		newGate.input = [2]*wire{wires[0], wires[1]}
		newGate.output = wires[2]

		wires[0].output = append(wires[0].output, &newGate)
		wires[1].output = append(wires[1].output, &newGate)
		wires[2].input = &newGate
	}
}

func main() {
	parse(os.Stdin)

	data.solve()
	P1 := data.zScore
	P2 := 0

	fmt.Printf("P1: %d\n", P1)
	fmt.Printf("P2: %d\n", P2)
}
