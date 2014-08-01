#!/bin/bash

# http://marc.info/?l=imagemagick-user&m=120944276824836&w=2 image magick q32 necessary

X="${X:-500}"
Y="${Y:-$X}"
DX="${DX:-1000}"
DY="${DY:-$DX}"
GEOMETRY="${GEOMETRY:-$( printf %sx%s+%s+%s $DX $DY $X $Y )}"
BASE_NAME="${BASE_NAME:-result_%06d.tif}"
SOURCE_DIR="${SOURCE_DIR:-2000x2000/data}"
TARGET_DIR="${TARGET_DIR:-$GEOMETRY/data}"
START="${START:-750}"
STOP="${STOP:-1049}"

mkdir -p $TARGET_DIR


for i in $(seq "$START" "$STOP")
do
    echo $i
    FILE="$(printf $BASE_NAME $i)"
    python -c "import vigra; img = vigra.impex.readImage('$SOURCE_DIR/$FILE'); vigra.impex.writeImage( img[$X:$X+$DX,$Y:$Y+$DY,...], '$TARGET_DIR/$FILE' )"
done


