package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
)

type disk struct {
	diskMap    []int
	expanded   []int
	freeSpaces []int
}

var diskState = disk{}

func (s *disk) expand() {
	curr := 0

	for i, length := range s.diskMap {
		if i%2 == 0 {
			for range length {
				s.expanded = append(s.expanded, i/2)
			}
		} else {
			for i := range length {
				s.expanded = append(s.expanded, -1)
				s.freeSpaces = append(s.freeSpaces, curr+i)
			}
		}

		curr += length
	}

	return
}

func (s *disk) fragment() {
	j := 0
	for i := len(s.expanded) - 1; i > -1; i-- {
		if j == len(s.freeSpaces) {
			break
		}

		pop := s.expanded[i]
		for pop == -1 {
			i--
			pop = s.expanded[i]
		}

		s.expanded[s.freeSpaces[j]] = pop
		j++
	}

	s.expanded = s.expanded[:len(s.expanded)-len(s.freeSpaces)]
}

func (s *disk) checksum() (res int) {
	for i, id := range diskState.expanded {
		res += i * id
	}

	return
}

func parse(r io.Reader) {
	reader := bufio.NewReader(r)
	buf, _ := reader.ReadString('\n')
	for _, r := range buf[:len(buf)-1] {
		diskState.diskMap = append(diskState.diskMap, int(r)-48)
	}
}
func main() {
	parse(os.Stdin)
	diskState.expand()
	diskState.fragment()

	P1 := diskState.checksum()
	P2 := 0

	fmt.Printf("P1: %d\n", P1)
	fmt.Printf("P2: %d\n", P2)
}
