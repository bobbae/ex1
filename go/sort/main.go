package main

import (
	"fmt"
	"sort"
)

type Element struct {
	Name string
	Index int
}

func InsertSorted(s []Element, e Element) []Element {
	ne := Element{}
	s = append(s, ne)
	i := sort.Search(len(s), func(i int) bool { return s[i].Index > e.Index })
	copy(s[i+1:], s[i:])
	s[i] = e
	return s
}

func main() {
	e1:= Element{Name: "one", Index: 1}
	e2:= Element{Name: "two", Index: 2}
	e8:= Element{Name: "eight", Index: 8}
	e9:= Element{Name: "nine", Index: 9}
	s := []Element{e1,e2,e8,e9}
	e5:= Element{Name: "five", Index: 5}
	s = InsertSorted(s,e5)
	fmt.Println(s)
}
