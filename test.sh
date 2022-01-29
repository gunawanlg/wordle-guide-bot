#!/bin/bash

for x in {1..1000}; do
    python test.py > log/out$x.log &
    pids[${x}]=$!
done

# wait for all pids
for pid in ${pids[*]}; do
    wait $pid
done

cat log/*.log > $1
rm -rf log/*