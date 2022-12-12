sudo socat TCP-LISTEN:80,reuseaddr,fork,su=nobody TCP:localhost:8080
#socat -vv OPENSSL-LISTEN:443,cert=cert.pem,cafile=cacert.pem,cert=cert.key,reuseaddr,fork TCP4:192.168.34.65:80
