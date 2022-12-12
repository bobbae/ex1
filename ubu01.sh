
ssh -l ubuntu `multipass list --format json | jq '.list[] | select(.name=="ubu01") | .ipv4[0]' | sed -e 's/"//g'`
