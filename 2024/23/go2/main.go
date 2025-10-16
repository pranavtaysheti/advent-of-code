package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"slices"
	"strings"
)

type nodeName [2]byte

func (n nodeName) value() (res int) {
	return int(n[0]-96)*26 + int(n[1])
}

type node struct {
	nodeName
	connections map[*node]struct{}
}

func cmpNode(n1 *node, n2 *node) int {
	return n1.value() - n2.value()
}

func makeNode(name nodeName) *node {
	return &node{
		nodeName:    name,
		connections: map[*node]struct{}{},
	}
}

func shapeValue(s []*node) string {
	res := make([]byte, len(s)*2)
	slices.SortFunc(s, cmpNode)
	for i, n := range s {
		res[i*2] = n.nodeName[0]
		res[i*2+1] = n.nodeName[1]
	}

	return string(res)
}

type graph struct {
	nodes  map[int]*node
	shapes []map[string][]*node
}

func (g graph) add(ns1, ns2 string) {
	nn1, nn2 := nodeName{ns1[0], ns1[1]}, nodeName{ns2[0], ns2[1]}
	nv1, nv2 := nn1.value(), nn2.value()

	var n1, n2 *node

	if _, ok := data.nodes[nv1]; !ok {
		n1 = makeNode(nn1)
		data.nodes[nv1] = n1
	} else {
		n1 = data.nodes[nv1]
	}

	if _, ok := data.nodes[nv2]; !ok {
		n2 = makeNode(nn2)
		data.nodes[nv2] = n2
	} else {
		n2 = data.nodes[nv2]
	}

	n1.connections[n2] = struct{}{}
	n2.connections[n1] = struct{}{}

	edge := []*node{n1, n2}
	data.shapes[0][shapeValue(edge)] = edge
}

func (g *graph) study(degree int) {
	g.shapes = append(g.shapes, map[string][]*node{})

	for _, shape := range g.shapes[degree-3] {
		prevCommonNodes := map[*node]struct{}{}
		for n := range shape[0].connections {
			prevCommonNodes[n] = struct{}{}
		}

		for _, n := range shape[1:] {
			commonNodes := map[*node]struct{}{}
			for i := range n.connections {
				if _, ok := prevCommonNodes[i]; ok {
					commonNodes[i] = struct{}{}
				}
			}

			prevCommonNodes = commonNodes
		}

		for n := range prevCommonNodes {
			nodes := []*node{n}
			nodes = append(nodes, shape...)
			g.shapes[degree-2][shapeValue(nodes)] = nodes
		}
	}
}

func (g *graph) solve() {
	for i := 3; len(g.shapes[i-3]) > 0; i++ {
		(*g).study(i)
	}
}

var data = graph{
	nodes:  map[int]*node{},
	shapes: []map[string][]*node{{}},
}

func parse(r io.Reader) {
	scanner := bufio.NewScanner(r)
	for scanner.Scan() {
		n := strings.Split(scanner.Text(), "-")
		data.add(n[0], n[1])
	}
}

func main() {
	parse(os.Stdin)
	data.solve()

	P1 := 0
	for t := range data.shapes[1] {
		for i, r := range t {
			if i%2 != 0 {
				continue
			}

			if r == 't' {
				P1++
				break
			}
		}
	}

	fmt.Printf("P1: %d\n", P1)

	P2Raw := []string{}
	for s := range data.shapes[len(data.shapes)-2] {
		curr := []rune{}
		for i, r := range s {
			if i%2 == 0 {
				P2Raw = append(P2Raw, string(curr))
				curr = make([]rune, 2)
			}

			curr = append(curr, r)
		}

		P2Raw = append(P2Raw, string(curr))
		break
	}
	
	P2 := strings.Join(P2Raw[1:], ",")
	fmt.Printf("P2: %v\n", P2)
}
