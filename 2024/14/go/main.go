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

type robot struct {
	position [2]int
	velocity [2]int
}

func (r robot) newPosition(time int, floorDimensions [2]int) (res [2]int) {
	height, width := floorDimensions[0], floorDimensions[1]

	correct := func(v, m int) int {
		v = v % m
		if v < 0 {
			return m + v
		}

		return v
	}

	res[0] = correct((r.position[0] + time*r.velocity[0]), height)
	res[1] = correct((r.position[1] + time*r.velocity[1]), width)

	return
}

type floor struct {
	robots     map[robot]struct{}
	dimensions [2]int
}

func (f floor) score(time int) int {
	return state{&f, slices.Collect(f.newPositions(time))}.score()
}

func (f floor) newPositions(time int) iter.Seq[[2]int] {
	return func(yield func([2]int) bool) {
		for r := range f.robots {
			if !yield(r.newPosition(time, f.dimensions)) {
				break
			}
		}
	}
}

func (f floor) simulate() iter.Seq2[int, [][2]int] {
	return func(yield func(int, [][2]int) bool) {
		for time := range math.MaxInt16 {
			if !yield(time, slices.Collect(f.newPositions(time))) {
				break
			}
		}
	}
}

func (f floor) print(time int) {
	region := make([][]rune, f.dimensions[0])
	for i := range f.dimensions[0] {
		region[i] = make([]rune, f.dimensions[1])

		for j := range f.dimensions[1] {
			region[i][j] = ' '
		}
	}

	for pos := range f.newPositions(time) {
		region[pos[0]][pos[1]] = '#'
	}

	for _, line := range region {
		fmt.Println(string(line))
	}

}

type state struct {
	floor     *floor
	positions [][2]int
}

func (s state) score() int {
	height, width := s.floor.dimensions[0], s.floor.dimensions[1]

	q1, q2, q3, q4 := 0, 0, 0, 0
	for _, newPos := range s.positions {

		switch {
		case newPos[0] < height/2 && newPos[1] > width/2:
			q1++
		case newPos[0] < height/2 && newPos[1] < width/2:
			q2++
		case newPos[0] > height/2 && newPos[1] < width/2:
			q3++
		case newPos[0] > height/2 && newPos[1] > width/2:
			q4++
		}
	}

	return q1 * q2 * q3 * q4
}

func (s state) standardDeviation() [2]float64 {
	calc := func(index int) float64 {
		var sum float64
		for _, p := range s.positions {
			sum += float64(p[index])
		}

		mean := sum / float64(len(s.positions))

		var numerator float64
		for _, p := range s.positions {
			numerator += math.Pow((float64(p[index]) - mean), 2)
		}

		return numerator / float64(len(s.positions))

	}

	return [2]float64{calc(0), calc(1)}

}

var data = floor{robots: map[robot]struct{}{}}

func parse(r io.Reader) {
	scanner := bufio.NewScanner(r)

	for scanner.Scan() {
		fields := strings.Fields(scanner.Text())

		posNums := strings.Split(fields[0][2:], ",")
		velocityNums := strings.Split(fields[1][2:], ",")

		posX, _ := strconv.Atoi(posNums[0])
		posY, _ := strconv.Atoi(posNums[1])

		velocityX, _ := strconv.Atoi(velocityNums[0])
		velocityY, _ := strconv.Atoi(velocityNums[1])

		data.robots[robot{
			[2]int{posY, posX},
			[2]int{velocityY, velocityX}}] = struct{}{}
	}
}

func main() {
	parse(os.Stdin)
	data.dimensions = [2]int{103, 101}

	P1 := data.score(100)

	var P2 int
	for time, positions := range data.simulate() {
		v := state{&data, positions}.standardDeviation()
		if v[0] < 450 && v[1] < 450 {
			P2 = time
			break
		}
	}

	fmt.Printf("P1: %d\n", P1)
	fmt.Printf("P2: %d\n", P2)

	data.print(P2)
}
