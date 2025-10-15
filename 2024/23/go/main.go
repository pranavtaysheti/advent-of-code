package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"slices"
	"strings"
)

type node [2]byte

func cmpNode(n1, n2 node) int {
	return n1.hash() - n2.hash()
}

func (n node) hash() (res int) {
	for _, r := range n {
		res *= 26
		res += int(r) - 96
	}

	return res
}

type edge [2]node

func makeEdge(n1, n2 node) edge {
	res := []node{n1, n2}
	slices.SortFunc(res, cmpNode)
	return edge(res)
}

type triangle [3]node

func makeTriangle(n1, n2, n3 node) triangle {
	res := []node{n1, n2, n3}
	slices.SortFunc(res, cmpNode)
	return triangle(res)
}

type graph struct {
	nodes        map[node]struct{}
	edges        map[edge]struct{}
	triangles    map[triangle]struct{}
	incTriangles map[edge]map[node]triangle
}

func makeGraph() graph {
	return graph{
		nodes:        map[node]struct{}{},
		edges:        map[edge]struct{}{},
		triangles:    map[triangle]struct{}{},
		incTriangles: map[edge]map[node]triangle{},
	}
}

func (g *graph) add(s1 string, s2 string) {
	n1, n2 := node([]byte(s1)), node([]byte(s2))
	g.nodes[n1] = struct{}{}
	g.nodes[n2] = struct{}{}

	newEdge := makeEdge(n1, n2)

	g.edges[newEdge] = struct{}{}

	if m, ok := g.incTriangles[newEdge]; ok {
		for n, t := range m {
			g.triangles[t] = struct{}{}
			delete(m, n)
		}

		delete(g.incTriangles, newEdge)
	}

	addIncTriangle := func(n1, n2, n3 node) {
		newTriangle := makeTriangle(n1, n2, n3)
		missingEdge := makeEdge(n1, n2)

		_, ok := g.incTriangles[missingEdge]
		if !ok {
			g.incTriangles[missingEdge] = map[node]triangle{}
		}

		g.incTriangles[missingEdge][n3] = newTriangle
	}

	for v := range g.edges {
		cn1, cn2 := v[0], v[1]
		switch {
		case n1 == cn1:
			addIncTriangle(n2, cn2, n1)
		case n1 == cn2:
			addIncTriangle(n2, cn1, n1)
		case n2 == cn1:
			addIncTriangle(n1, cn2, n2)
		case n2 == cn2:
			addIncTriangle(n1, cn1, n2)
		}
	}
}

var data = makeGraph()

func parse(r io.Reader) {
	scanner := bufio.NewScanner(r)
	for scanner.Scan() {
		nodeNames := strings.Split(scanner.Text(), "-")
		s1, s2 := nodeNames[0], nodeNames[1]
		data.add(s1, s2)
	}
}

func main() {
	parse(os.Stdin)

	P1 := 0
	for t := range data.triangles {
		for _, n := range t {
			if n[0] == 't' {
				P1++
				break
			}
		}
	}

	fmt.Printf("P1: %d\n", P1)

	P2 := 0

	fmt.Printf("P2: %d\n", P2)
}
