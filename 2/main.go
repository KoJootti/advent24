package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

const test_data_file string = "input.txt"

type Report struct {
	data []int
}

func getReport(line string) *Report {
	r := new(Report)
	r.data = make([]int, 0)
	values := strings.Fields(line)
	for _, value := range values {
		val, err := strconv.Atoi(value)
		if err != nil {
			fmt.Println(err)
			panic(err)
		}
		r.data = append(r.data, val)
	}
	return r
}

func absDiffInt(a, b int) int {
	if a > b {
		return a - b
	}
	return b - a
}

func pointsDiffSafe(a, b int, asc bool) bool {
	diff := absDiffInt(a, b)
	if diff < 1 || diff > 3 {
		return false
	}
	if asc && b < a {
		return false
	}
	if !asc && b > a {
		return false
	}
	return true
}

func isSafe(data []int) (bool, int, int) {
	len := len(data)
	asc := true

	if len < 2 {
		return true, 0, 1
	}

	firstVal := data[0]
	prevVal := data[1]

	if prevVal < firstVal {
		asc = false
	}

	if !pointsDiffSafe(firstVal, prevVal, asc) {
		return false, 0, 1
	}

	for idx, val := range data[2:] {
		if !pointsDiffSafe(prevVal, val, asc) {
			return false, idx + 1, idx + 2
		}
		prevVal = val
	}
	return true, 0, 0
}

func (r *Report) DataWithoutIndex(i int) []int {
	newSlice := make([]int, len(r.data))
	copy(newSlice, r.data)
	return append(newSlice[:i], newSlice[i+1:]...)
}

func main() {
	reports := make([]*Report, 0)
	file, err := os.Open(test_data_file)

	if err != nil {
		fmt.Println(err)
		panic(err)
	}

	defer file.Close()

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		reports = append(reports, getReport(line))
	}

	sum := 0
	n := 0
	for _, report := range reports {
		n++
		safe, idx1, idx2 := isSafe(report.data)
		if safe {
			sum++
		} else {
			//fmt.Printf("Data: %v, idx1: %d, idx2: %d\n", report.data, idx1, idx2)
			wOidx1 := report.DataWithoutIndex(idx1)
			wOidx2 := report.DataWithoutIndex(idx2)
			//fmt.Printf("Data without idx1: %v, Data without idx2: %v\n", wOidx1, wOidx2)
			isSafe1, _, _ := isSafe(wOidx1)
			isSafe2, _, _ := isSafe(wOidx2)
			if isSafe1 || isSafe2 {
				sum++
			}
		}
	}
	fmt.Printf("Total: %d, Safe amount: %d\n", n, sum)
}
