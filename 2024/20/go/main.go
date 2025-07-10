package main

import (
	"bufio"
	"fmt"
	"io"
	"iter"
	"math"
	"os"
	"strings"
)

const MIN_TIME = 100

type vector [2]int

func (v vector) distance() int {
	return max(-v[0], v[0]) + max(-v[1], v[1])
}

func (v vector) add(a vector) vector {
	return [2]int{v[0] + a[0], v[1] + a[1]}
}

func (v vector) substract(s vector) vector {
	return [2]int{v[0] - s[0], v[1] - s[1]}
}

var directions = [4]vector{
	{-1, 0},
	{0, +1},
	{+1, 0},
	{0, -1},
}

type raceTrack struct {
	start [2]int
	end   [2]int
	track [][]int
	path  []vector
}

type cheat struct {
	start [2]int
	end   [2]int
}

func (r *raceTrack) prime() {
	r.path = append(r.path, r.start)

	for i, c := 0, r.start; c != r.end; i++ {
		for _, d := range directions {
			n_pos := d.add(c)
			n_row, n_col := n_pos[0], n_pos[1]

			if r.track[n_row][n_col] == 0 {
				r.track[n_row][n_col] = i + 1
				c = [2]int{n_row, n_col}
				r.path = append(r.path, c)
				break
			}
		}
	}
}

func combinations[T any](l []T) iter.Seq[[2]T] {
	return func(yield func([2]T) bool) {
		for i := range len(l) - 1 {
			for j := range len(l) - 1 - i {
				if !yield([2]T{l[i], l[i+j+1]}) {
					return
				}
			}
		}
	}
}
func (r raceTrack) findCheats2(time int) map[int]int {
	res := map[int]int{}

	i := 0
	for v := range combinations(r.path) {
		v0_steps, v1_steps := r.track[v[0][0]][v[0][1]], r.track[v[1][0]][v[1][1]]

		var dist = v[0].substract(v[1]).distance()
		if dist < 0 {
			dist = -dist
		}

		var diff = v0_steps - v1_steps
		if diff < 0 {
			diff = -diff
		}

		if dist > time || diff == dist {
			continue
		}

		time_saved := diff - dist

		v, ok := res[time_saved]
		if !ok {
			res[time_saved] = 1
		} else {
			res[time_saved] = v + 1
		}

		i++
	}

	return res
}

func parse(r io.Reader) (m raceTrack) {
	scanner := bufio.NewScanner(r)

	for i := 0; scanner.Scan(); i++ {
		line := scanner.Text()

		if j := strings.IndexRune(line, 'S'); j > -1 {
			m.start = [2]int{i, j}
		}

		if j := strings.IndexRune(line, 'E'); j > -1 {
			m.end = [2]int{i, j}
		}

		m.track = append(m.track, make([]int, len(line)))
		for j, r := range line {
			if r == '#' {
				m.track[i][j] = math.MaxInt
			} else {
				m.track[i][j] = 0
			}
		}

	}

	return
}

func totalCheats(d raceTrack, max_time int) (res int) {
	for time_saved, q := range d.findCheats2(max_time) {
		if time_saved >= MIN_TIME {
			res += q
		}
	}

	return
}
func main() {
	data := parse(os.Stdin)
	data.prime()

	P1 := totalCheats(data, 2)
	P2 := totalCheats(data, 20)

	fmt.Printf("P1: %d\n", P1)
	fmt.Printf("P2: %d\n", P2)
}
