#!/bin/bash

name=`hostname`
if [[ "$name" -eq "Conan" ]]; then
    xrandr --output VGA1 --auto --right-of DVI1
fi
