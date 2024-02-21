package main

import "fmt"

type pp struct {
	Name string
}

func main() {
	var pt1 pp
	pt1.Name = "foo"
	pt2 := func1(&pt1) //pass pointer
	fmt.Print(pt1, pt2)

	pt1.Name = "foo"
	pt2 = func2(pt1) //pass value
	fmt.Print(pt1, pt2)

}

func func1(pt1 *pp) (*pp) {
	pt1.Name = "bar"
	return pt1
}

func func2(pt1 pp) (*pp) {
	pt1.Name = "bar"
	return &pt1
}
