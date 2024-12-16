package main

import (
	"bufio"
	"fmt"
	"io"
	"iter"
	"os"
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
	height, width := f.dimensions[0], f.dimensions[1]

	q1, q2, q3, q4 := 0, 0, 0, 0
	for newPos := range f.newPositions(time) {
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

	fmt.Println(q1, q2, q3, q4)
	return q1 * q2 * q3 * q4
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

// func (f floor) simulate() iter.Seq2[int, map[robot]struct{}] {
// 	return func(yield func(int, map[robot]struct{}) bool) {
// 		for time, state := 0, maps.Clone(f.robots); ; time++ {
// 			for r := range state {
// 				r.position = r.newPosition(1, f.dimensions)
// 			}

// 			if !yield(time, state) {
// 				break
// 			}
// 		}
// 	}
// }

// func (f floor) simulateScore() int {
// 	for t, newF := range f.simulate() {
// 		if t == 100 {
// 			return newF.score(0)
// 		}
// 	}

// 	panic("this shouldnt happen")
// }

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
	P2 := 0

	fmt.Printf("P1: %d\n", P1)
	fmt.Printf("P2: %d\n", P2)
}
