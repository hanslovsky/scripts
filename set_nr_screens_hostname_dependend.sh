#!/bin/bash


# check xrandr output!

name=`hostname`
if [[ "$name" -eq "Conan" ]]; then
    xrandr --output VGA1 --auto --right-of DVI1
fi

if [[ "$name" -eq "Kaminsky" ]]; then
    xrandr --output DVI2 --auto --right-of DVI2
fi
