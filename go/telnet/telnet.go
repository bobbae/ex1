// telnet creates a new Expect spawner for Telnet.
package main

import (
	"flag"
	"regexp"
	"time"

	"github.com/bobbae/q"
	expect "github.com/google/goexpect"

	"github.com/golang/glog"
	"github.com/ziutek/telnet"
)

const (
	network = "tcp"
	timeout = 10 * time.Second
)

func main() {
	address := flag.String("address", "", "address of telnet server")
	user := flag.String("user", "", "username to use")
	password := flag.String("password", "", "password to use")

	userRE := regexp.MustCompile("username:")
	passRE := regexp.MustCompile("password:")
	promptRE := regexp.MustCompile("#")

	flag.Parse()

	exp, _, err := telnetSpawn(*address, timeout, expect.Verbose(true))
	if err != nil {
		glog.Exitf("telnetSpawn(%q,%v) failed: %v", *address, timeout, err)
	}

	defer func() {
		if err := exp.Close(); err != nil {
			glog.Infof("exp.Close failed: %v", err)
		}
	}()

	exp.Expect(userRE, timeout)
	exp.Send(*user + "\n")
	exp.Expect(passRE, timeout)
	exp.Send(*password + "\n")
	exp.Expect(promptRE, timeout)
	exp.Send("configure\n")
	exp.Expect(promptRE, timeout)
	exp.Send("show ip\n")
	result, _, _ := exp.Expect(promptRE, timeout)

	q.Q(result)

}

func telnetSpawn(addr string, timeout time.Duration, opts ...expect.Option) (expect.Expecter, <-chan error, error) {
	conn, err := telnet.Dial(network, addr)
	if err != nil {
		return nil, nil, err
	}

	resCh := make(chan error)

	return expect.SpawnGeneric(&expect.GenOptions{
		In:  conn,
		Out: conn,
		Wait: func() error {
			return <-resCh
		},
		Close: func() error {
			close(resCh)
			return conn.Close()
		},
		Check: func() bool { return true },
	}, timeout, opts...)
}
