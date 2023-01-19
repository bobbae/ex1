package main

import (
	"fmt"
	"sync"

	"github.com/qeof/q"
)

type Mydata struct {
	name  string
	value int
}

func init() {
	q.O = "stderr"
	q.P = ".*"
}

func main() {
	var wg sync.WaitGroup
	var m sync.Map

	wg.Add(5)
	for i := 0; i < 5; i++ {
		go func(j int) {
			mdata := Mydata{name: fmt.Sprintf("test_%v", j), value: i}
			m.Store(mdata.name, mdata)
			wg.Done()
		}(i)
	}

	wg.Wait()
	fmt.Println("Done.")

	for i := 0; i < 5; i++ {
		t, ok := m.Load(i)
		if !ok {
			q.Q(i, "missing")
			continue
		}
		q.Q(t)
	}

	m.Range(func(k, v interface{}) bool {
		q.Q(k, v)
		return true
	})
}
