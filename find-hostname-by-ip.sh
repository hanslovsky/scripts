#!/bin/bash

CWD="$PWD"
# LOG_DIR something like ~/.spark/logs/<timestamp>
LOG_DIR="$1"
IP_ADDR="$2"

cd $LOG_DIR

for fn in h*.out; do
    HN=`echo $fn | grep -Eo '^[^\.]+'`
    ssh -x $HN '/sbin/ip addr | grep "10.38.104.35" && hostname'
done

cd $CWD
