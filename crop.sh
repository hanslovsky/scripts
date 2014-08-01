#!/bin/bash

X="${X:-2500}"
Y="${Y:-$X}"
DX="${DX:-5000}"
DY="${DY:-$DX}"
GEOMETRY="${GEOMETRY:-$( printf %sx%s+%s+%s $DX $DY $X $Y )}"
BASE_NAME="${BASE_NAME:-result_%06d.tif}"
SOURCE_DIR="${SOURCE_DIR:-10000x10000}"
TARGET_DIR="${TARGET_DIR:-$GEOMETRY/data}"
START="${START:-750}"
STOP="${STOP:-1049}"

echo $TARGET_DIR
exit 1

mkdir -p $TARGET_DIR

for i in $(seq "$START" "$STOP")
do
    echo $i
    FILE="$(printf $BASE_NAME $i)"
    convert "$SOURCE_DIR/$FILE" -depth 32 -crop "$GEOMETRY" "$TARGET_DIR/$FILE"
done


