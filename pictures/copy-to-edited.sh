#!/usr/bin/env bash

EDITED=edited
mkdir -p $EDITED

for DIR in jpeg raw; do
    if [ -d "$DIR" ]; then
        for SOURCE in $DIR/*_v*.JPG; do
            FILENAME=$(basename $SOURCE .JPG)
            TARGET=$EDITED/${FILENAME}.${DIR}.JPG
            if [ -e "$TARGET" -a -z "$OVERWRITE_EXISTING" ]; then
                echo "Skipping $SOURCE -> $TARGET"
            else
                cp $SOURCE $TARGET
            fi
        done
    fi
done
