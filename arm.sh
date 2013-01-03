#!/bin/bash

set -e

OLD_LD=$LD_LIBRARY_PATH
OLD_LIBRARY=$LIBRARY_PATH
OLD_PATH=$PATH
OLD_C=$C_INCLUDE_PATH
OLD_CPLUS=$CPLUS_INCLUDE_PATH

export LD_LIBRARY_PATH=$HOME/local/pi-x-compile/lib
export LIBRARY_PATH=$HOME/local/pi-x-compile/lib
export PATH=$HOME/local/pi-x-compile/bin:$HOME/x-tools-arm/{arm-unknown-linux-gnueabi}/bin:$PATH
export C_INCLUDE_PATH=$HOME/local/pi-x-compile/include
export CPLUS_INCLUDE_PATH=$HOME/local/pi-x-compile/include

CXX=arm-unknown-linux-gnueabi-g++ CC=arm-unknown-linux-gnueabi-gcc ./configure --prefix=/home/phil/local/pi-x-compile --host=amd64-linux --build=arm

export LD_LIBRARY_PATH=$OLD_LD
export LIBRARY_PATH=$OLD_LIBRARY
export PATH=$OLD_PATH
export C_INCLUDE_PATH=$OLD_C
export CPLUS_INCLUDEPATH=$OLD_CPLUS
