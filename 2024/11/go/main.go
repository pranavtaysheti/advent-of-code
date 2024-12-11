package main

import (
	"bufio"
	"fmt"
	"io"
	"math"
	"os"
	"strconv"
)

type stone int

func (s stone) solve(times int) int {
	type memoKey struct {
		num int
		times int
	}

	memo := map[memoKey]int {}

	var blink func(int, int) int
	blink = func (num int, times int) int {
		memoize := func(length int) int {
			memo[memoKey{num, times}] = length
			return length
		}

		if length, ok := memo[memoKey{num, times}]; ok {
			return length
		}

		if times == 0 {
			return 1
		}

		if num == 0 {
			return memoize(blink(1, times-1))
		}

		if digits := int(math.Ceil(math.Log10(float64(num + 1)))); digits%2 == 0 {
			P1 := num / int(math.Pow10(digits/2))
			P2 := num % int(math.Pow10(digits/2))

			return memoize(blink(P1, times-1) + blink(P2, times-1))
		}

		return memoize(blink(num*2024, times-1))
	}

	return blink(int(s), times)
}

type stoneSlice []stone

func (sSlice stoneSlice) blink(times int) (res int) {
	for _, s := range sSlice {
		res += s.solve(times)
	}

	return res
}

var data = stoneSlice{}

func parse(r io.Reader) {
	scanner := bufio.NewScanner(r)
	scanner.Split(bufio.ScanWords)

	for scanner.Scan() {
		num, _ := strconv.Atoi(scanner.Text())
		data = append(data, stone(num))
	}
}

func main() {
	parse(os.Stdin)

	P1 := data.blink(25)
	P2 := data.blink(75)
	
	fmt.Printf("P1: %d\n", P1)
	fmt.Printf("P2: %d\n", P2)
}
