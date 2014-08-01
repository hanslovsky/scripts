#!/bin/bash

cwd="$( realpath $PWD )"
DELETE_OLD="${DELETE_OLD:-}"
TARGET_DIR=${TARGET_DIR:-$HOME/local/bin}

mkdir -p "$TARGET_DIR"
TARGET_DIR="$( realpath $TARGET_DIR )"

if [ -z "$DELETE_OLD" ]; then
    find . -maxdepth 1 -type f -not -name 'install.sh' -not -name '.git' -executable -execdir ln -s "$cwd/"{} "$TARGET_DIR" \;
else
    find . -maxdepth 1 -type f -not -name 'install.sh' -not -name '.git' -executable \( -execdir rm "$TARGET_DIR"/{} \; , -execdir ln -s "$cwd/"{} "$TARGET_DIR" \; \)
fi
