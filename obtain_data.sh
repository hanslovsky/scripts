#!/bin/bash

SOURCE_DIR="$( realpath ${SOURCE_DIR:-/nobackup/saalfeld/philipp/playground/pov-ray/no_wave/scale/variable/1/4/tif} )"
TARGET_DIR="$( realpath ${TARGET_DIR:-/ssd/hanslovskyp/playground/pov-ray/variable_thickness_subset1/750-1049/scale/1.0/10000x10000/data} )"
FILE_PATTERN="${FILE_PATTERN:-result_%06d.tif}"
START="${START:-750}"
END="${END:-1049}"
N="$(( $END - $START ))"
COUNT=0

for index in $( seq $START $END ); do
    FILE="$SOURCE_DIR/$( printf $FILE_PATTERN $index )"
    echo -e "$FILE ~> $TARGET_DIR\t\t$COUNT/$N\t($(( 100 * $COUNT / $N )))"
    cp "$FILE" "$TARGET_DIR"
    COUNT="$(( $COUNT + 1 ))"
done

