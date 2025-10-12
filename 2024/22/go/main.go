package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"strconv"
)

const histLen = 4
const pruneNumber = 1<<24 - 1
const snGenerated = 2000

type secretNumber int

func (sn secretNumber) generate() secretNumber {
	n_sn := sn << 6
	sn = n_sn ^ sn
	sn = sn & pruneNumber

	n_sn = sn >> 5
	sn = n_sn ^ sn
	sn = sn & pruneNumber

	n_sn = sn << 11
	sn = n_sn ^ sn
	sn = sn & pruneNumber

	return sn
}

func (sn secretNumber) generateAll() generatedNumbers {
	res := make([]secretNumber, snGenerated+1)
	res[0] = sn
	for i := range snGenerated {
		sn = sn.generate()
		res[i+1] = sn
	}

	return res
}

type priceObservations map[[histLen]int8]int

func (s priceObservations) maxProfit() int {
	currMax := 0
	for _, p := range s {
		currMax = max(currMax, p)
	}

	return currMax
}

type generatedNumbers []secretNumber

func (l generatedNumbers) observe() priceObservations {
	curr := [histLen]int8{}
	res := priceObservations{}

	//Prime the initial 4 secretNumbers
	for i := range histLen {
		curr[i] = int8(l[i+1]%10 - l[i]%10)
	}

	res[curr] = int(l[histLen] % 10)

	//Rest of the secretNumbers
	for i := range len(l) - histLen - 1 {
		for j := range histLen - 1 {
			curr[j] = curr[j+1]
		}

		curr[histLen-1] = int8(l[histLen+i+1]%10 - l[histLen+i]%10)

		if _, ok := res[curr]; !ok {
			res[curr] = int(l[histLen+i+1] % 10)
		}
	}

	return res
}

var secretNumbers []secretNumber

func parse(r io.Reader) {
	scanner := bufio.NewScanner(r)
	for scanner.Scan() {
		num, _ := strconv.Atoi(scanner.Text())
		secretNumbers = append(secretNumbers, secretNumber(num))
	}
}

func main() {
	parse(os.Stdin)

	allMonkeyNumbers := make([]generatedNumbers, len(secretNumbers))

	for i, n := range secretNumbers {
		allMonkeyNumbers[i] = n.generateAll()
	}

	P1 := 0
	for _, n := range allMonkeyNumbers {
		P1 += int(n[snGenerated])
	}

	fmt.Printf("P1: %d\n", P1)

	res := priceObservations{}
	for _, gn := range allMonkeyNumbers {
		for hist, num := range gn.observe() {
			if v, ok := res[hist]; !ok {
				res[hist] = num
			} else {
				res[hist] = num + v
			}
		}
	}

	P2 := res.maxProfit()
	fmt.Printf("P2: %d\n", P2)
}
