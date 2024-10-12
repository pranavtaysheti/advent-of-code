package main

import (
	"bufio"
	"errors"
	"fmt"
	"log"
	"math"
	"os"
	"reflect"
	"slices"
	"strconv"
	"strings"
)

type springState uint8
type springStateSlice []springState
type counts []int

const (
	ssNil springState = iota
	ssUnknown
	ssOperational
	ssDamaged
)

type RecordEntry struct {
	springs springStateSlice
	counts  counts
}

var data []RecordEntry

func (s springStateSlice) counts() (r counts) {
	isOperational := (s[0] == ssOperational)
	prev := 0

	for i, c := range s {
		if c == ssOperational {
			if isOperational == false {
				r = append(r, i-prev)
				isOperational = true
			}
		}
		if slices.Contains([]springState{ssDamaged, ssUnknown}, c) {
			if isOperational == true {
				prev = i
				isOperational = false
			}
		}
	}

	if isOperational == false {
		r = append(r, len(s)-prev)
	}

	return
}

func (s springStateSlice) posUnknown() (r []int) {
	for i, e := range s {
		if e == ssUnknown {
			r = append(r, i)
		}
	}
	return
}

func permutations(l int) func() (r []bool, err error) {
	i := 0
	iMax := int(math.Pow(2, float64(l)))

	return func() ([]bool, error) {
		c := i
		if c == iMax {
			return nil, errors.New("iteration reached end")
		}

		r := make([]bool, l)
		pos := len(r) - 1
		for c > 0 {
			r[pos] = c%2 != 0
			c = int(math.Floor(float64(c / 2)))
			pos--
		}
		i++
		return r, nil
	}
}

func (s springStateSlice) substitute(n []bool) (springStateSlice, error) {
	pos := s.posUnknown()
	if len(n) > len(pos) {
		return nil, errors.New("size of substitution slice larger than SSUnkown")
	}

	r := make(springStateSlice, len(s))
	copy(r, s)

	for i := range len(n) {
		if n[i] == true {
			r[pos[i]] = ssOperational
		} else {
			r[pos[i]] = ssDamaged
		}
	}

	return r, nil
}
func (s springStateSlice) permutations() func() (springStateSlice, error) {
	posUnknown := s.posUnknown()
	permutationsIter := permutations(len(posUnknown))

	return func() (springStateSlice, error) {
		subPos, err := permutationsIter()
		if err != nil {
			return nil, err
		}

		subS, err := s.substitute(subPos)
		if err != nil {
			return nil, err
		}

		return subS, nil
	}

}

func verifyPermutation(i *int, p springStateSlice, c counts) {
	if reflect.DeepEqual(p.counts(), c) {
		*i++
	}
}

func getspringState(c rune) (springState, error) {
	switch c {
	case '?':
		return ssUnknown, nil
	case '.':
		return ssOperational, nil
	case '#':
		return ssDamaged, nil
	default:
		return ssNil, errors.New(fmt.Sprintf("unidentified spring state char %c", c))
	}
}

func getspringStateAll(s string) (r []springState, err error) {
	for i, c := range s {
		ss, err := getspringState(c)
		if err != nil {
			return r, errors.Join(
				errors.New(fmt.Sprintf("error on char %d", i)),
				err,
			)
		}

		r = append(r, ss)
	}

	return
}

func getCountAll(s string) (r []int, err error) {
	for i, c := range strings.Split(s, ",") {
		num, err := strconv.Atoi(c)
		if err != nil {
			return r, errors.Join(
				errors.New(fmt.Sprintf("error converting %q at %d", c, i)),
				err,
			)
		}

		r = append(r, num)
	}

	return
}

func parseRecord(r string) error {
	springStatesStr, countsStr, done := strings.Cut(r, " ")
	if !done {
		return errors.New("error cutting record string")
	}

	springStates, err := getspringStateAll(springStatesStr)
	if err != nil {
		return errors.Join(
			errors.New(fmt.Sprintf("error processing springs: %q", springStatesStr)),
			err,
		)
	}

	counts, err := getCountAll(countsStr)
	if err != nil {
		return errors.Join(
			errors.New(fmt.Sprintf("error processing counts: %q", countsStr)),
			err,
		)
	}

	data = append(data, RecordEntry{
		springs: springStates,
		counts:  counts,
	})
	return nil
}

func parseInput(s *bufio.Scanner) error {
	for i := 1; s.Scan(); i++ {
		err := parseRecord(s.Text())
		if err != nil {
			return errors.Join(
				errors.New(fmt.Sprintf("error parsing line %d", i)),
				err,
			)
		}
	}

	return s.Err()
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)

	err := parseInput(scanner)
	if err != nil {
		log.Fatalln(err)
	}

	P1 := 0

	for _, r := range data {
		permFunc := r.springs.permutations()
		for {
			s, err := permFunc()
			if err != nil {
				break
			}

			verifyPermutation(&P1, s, r.counts)
		}
	}
	P2 := 0

	fmt.Printf("P1: %d \n", P1)
	fmt.Printf("P2: %d \n", P2)
}
