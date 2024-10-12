package main

import (
	"errors"
	"fmt"
	"os"
	"strconv"
	"strings"
)

var input = make([]byte, 1024)
var data_p1 = make([]Race, 4)
var data_p2 = Race{}
var p1_sol = 1
var p2_sol int

type Race struct {
	time     int
	distance int
}

func parseNumberFields(l *string) []string {
	r := (*l)[9:]
	return strings.Fields(r)
}

func concatNumbers(nsl []string) (int, error) {
	return strconv.Atoi(strings.Join(nsl, ""))
}

func parseNumbers(l *string) (result []int) {
	for _, ns := range parseNumberFields(l) {
		n, err := strconv.Atoi(ns)
		if err != nil {
			panic("Error parsing numbers")
		}

		result = append(result, n)
	}

	return
}

func parseInput() {
	lines := strings.Split(string(input), "\n")
	times := parseNumbers(&lines[0])
	distances := parseNumbers(&lines[1])

	for i := 0; i < len(times); i++ {
		data_p1[i] = Race{
			time:     times[i],
			distance: distances[i],
		}
	}

	timeConcat, _ := concatNumbers(parseNumberFields(&lines[0]))
	distanceConcat, _ := concatNumbers(parseNumberFields(&lines[1]))

	data_p2 = Race{
		time:     timeConcat,
		distance: distanceConcat,
	}
}

func readInput() {
	input_temp, err := os.ReadFile("./input.txt")
	if err != nil {
		panic("Cannot read input file")
	}

	input = input_temp
}

func calcPeakHold(t int) float64 {
	return float64(t) / 2.0
}

func calcDistTravelled(t int, h int) int {
	return h * (t - h)
}

func calcHoldToBeatRecord(t int, r int) (int, error) {
	for i := 1; i < t; i++ {
		d := calcDistTravelled(t, i)
		if d > r {
			return i, nil
		}
	}

	return 0, errors.New("Impossible to beat record")
}

func calcWaysToBeatRecord(t int, r int) int {
	minHold, err := calcHoldToBeatRecord(t, r)
	if err != nil {
		return 0
	}

	peakHold := calcPeakHold(t)
	maxHold := minHold + int(2*(peakHold-float64(minHold)))
	return maxHold - minHold + 1

}

func solveP1() {
	for _, r := range data_p1 {
		t, d := r.time, r.distance
		p1_sol *= calcWaysToBeatRecord(t, d)
	}
}

func solveP2() {
	fmt.Println(data_p2)
	t, d := data_p2.time, data_p2.distance
	p2_sol = calcWaysToBeatRecord(t, d)
}

func main() {
	readInput()
	parseInput()
	solveP1()
	solveP2()
	fmt.Println("P1: ", p1_sol)
	fmt.Println("P2: ", p2_sol)
}
