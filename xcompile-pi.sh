#!/bin/bash

set -e

OLD_PATH=$PATH
USAGE="Usage: $0 -cxx|-c [compiler arguments]"
export PATH=/home/phil/x-tools-arm/{arm-unknown-linux-gnueabi}/bin
if [ "$#" == "0" ]; then
    echo $USAGE
elif [ "$1" == -cxx ]; then
    shift
    arm-unknown-linux-gnueabi-g++ $@
elif [ "$1" == -c ]; then
    shift
    arm-unknown-linux-gnueabi-gcc $@
else
    echo $USAGE
fi
export PATH=$OLD_PATH
unset OLD_PATH
