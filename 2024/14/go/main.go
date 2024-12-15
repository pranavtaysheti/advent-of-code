package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"strconv"
	"strings"
)

var height int
var width int

type robot struct {
	position [2]int
	velocity [2]int
}

func (r robot) newPosition(time int) (res [2]int) {
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

type floor []robot

func (f floor) score(time int) int {
	q1, q2, q3, q4 := 0, 0, 0, 0

	for _, r := range f {
		newPos := r.newPosition(time)

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

var data = floor{}

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

		data = append(data, robot{
			[2]int{posY, posX},
			[2]int{velocityY, velocityX}})
	}
}

func main() {
	parse(os.Stdin)

	height = 103
	width = 101

	P1 := data.score(100)
	P2 := 0

	fmt.Printf("P1: %d\n", P1)
	fmt.Printf("P2: %d\n", P2)
}
