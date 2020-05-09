#!/usr/bin/env bash

FACTOR=${FACTOR:-25%}

mkdir -p ${FACTOR}

for f in edited/*JPG; do
    bn=$(basename $f)
    target="${FACTOR}/$bn"
    if [ -e "$target" ]; then
        echo skipping $f
    else
        convert -resize ${FACTOR} $f $target
    fi
done
