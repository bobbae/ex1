

## Traffic control
```
tc qdisc add dev eth0 root handle 1: prio
tc filter add dev eth0 protocol ip parent 1: prio 1 u32 match ip dst 172.19.0.2 match ip dport 6363 0xffff flowid 1:1
tc filter add dev eth0 protocol all parent 1: prio 2 u32 match ip dst 0.0.0.0/0 flowid 1:2
tc filter add dev eth0 protocol all parent 1: prio 2 u32 match ip protocol 1 0xff flowid 1:2
tc qdisc add dev eth0 parent 1:1 handle 10: netem delay 10ms
tc qdisc add dev eth0 parent 1:2 handle 20: sfq

tc -s qdisc ls dev eth0
tc -s filter ls dev eth0
```
