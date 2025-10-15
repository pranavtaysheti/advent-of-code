package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"sort"
	"strings"
)

type node [2]byte

func (n node) hash() (res int) {
	for _, r := range n {
		res *= 26
		res += int(r) - 96
	}

	return res
}

type edge [2]node

func (e edge) hash() int {
	n1, n2 := e[0].hash(), e[1].hash()
	minVal := min(n1, n2)
	maxVal := max(n1, n2)

	return (maxVal << 10) + minVal
}

type triangle [3]node

func (t triangle) hash() int {
	n := []int{t[0].hash(), t[1].hash(), t[2].hash()}
	n = sort.IntSlice(n[:])
	return (n[0] << 20) + (n[1] << 10) + n[2]
}

type graph struct {
	nodes        map[node]struct{}
	edges        map[int]edge
	triangles    map[int]triangle
	incTriangles map[int]map[node]triangle
}

func makeGraph() graph {
	return graph{
		nodes:        map[node]struct{}{},
		edges:        map[int]edge{},
		triangles:    map[int]triangle{},
		incTriangles: map[int]map[node]triangle{},
	}
}

func (g *graph) add(s1 string, s2 string) {
	n1, n2 := node([]byte(s1)), node([]byte(s2))
	g.nodes[n1] = struct{}{}
	g.nodes[n2] = struct{}{}

	newEdge := edge{n1, n2}
	newEdgeHash := newEdge.hash()

	g.edges[newEdgeHash] = newEdge

	if m, ok := g.incTriangles[newEdgeHash]; ok {
		for n, t := range m {
			th := t.hash()
			g.triangles[th] = t
			delete(m, n)
		}

		delete(g.incTriangles, newEdgeHash)
	}

	for _, v := range g.edges {
		cn1, cn2 := v[0], v[1]
		switch {
		case n1 == cn1:
			newTriangle := triangle{cn1, cn2, n2}
			missingEdgeHash := edge{n2, cn2}.hash()

			_, ok := g.incTriangles[missingEdgeHash]
			if !ok {
				g.incTriangles[missingEdgeHash] = map[node]triangle{}
			}
			g.incTriangles[missingEdgeHash][n1] = newTriangle

		case n1 == cn2:
			newTriangle := triangle{cn1, cn2, n2}
			missingEdgeHash := edge{n2, cn1}.hash()

			_, ok := g.incTriangles[missingEdgeHash]
			if !ok {
				g.incTriangles[missingEdgeHash] = map[node]triangle{}
			}
			g.incTriangles[missingEdgeHash][n1] = newTriangle

		case n2 == cn1:
			newTriangle := triangle{cn1, cn2, n1}
			missingEdgeHash := edge{n1, cn2}.hash()

			_, ok := g.incTriangles[missingEdgeHash]
			if !ok {
				g.incTriangles[missingEdgeHash] = map[node]triangle{}
			}
			g.incTriangles[missingEdgeHash][n2] = newTriangle

		case n2 == cn2:
			newTriangle := triangle{cn1, cn2, n1}
			missingEdgeHash := edge{n1, cn1}.hash()

			_, ok := g.incTriangles[missingEdgeHash]
			if !ok {
				g.incTriangles[missingEdgeHash] = map[node]triangle{}
			}
			g.incTriangles[missingEdgeHash][n2] = newTriangle

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
	fmt.Println(len(data.triangles))
	P1 := 0
	for _, t := range data.triangles {
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
