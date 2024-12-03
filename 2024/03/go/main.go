package main

import (
	"fmt"
	"io"
	"os"
	"regexp"
	"strconv"
	"strings"
)

type memory string

func (m memory) solve() (do int, dont int) {
	reg := regexp.MustCompile(`(mul\(\d+,\d+\))|(do\(\))|(don't\(\))`)

	matches := reg.FindAll([]byte(m), -1)
	isDo := true
	for _, match := range matches {
		matchStr := string(match)

		if matchStr == "do()" {
			isDo = true
		} else if matchStr == "don't()" {
			isDo = false
		} else {
			matchStr = matchStr[4:len(matchStr)-1]
			numsStr := strings.Split(matchStr, ",")

			num1, _ := strconv.Atoi(numsStr[0])
			num2, _ := strconv.Atoi(numsStr[1])
			if isDo {
				do += num1 * num2
			} else {
				dont += num1 * num2
			}
		}
	}

	return
}

var data memory

func main() {
	buf, _ := io.ReadAll(os.Stdin)
	data = memory(buf)

	do, dont := data.solve()
	P1 := do + dont
	P2 := do

	fmt.Printf("P1: %d\n", P1)
	fmt.Printf("P2: %d\n", P2)
}
