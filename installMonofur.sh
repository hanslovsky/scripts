#!/bin/bash
cwd="$(pwd)"
TMPDIR="${TMPDIR:-/tmp}"
FONT_NAME="monofur"
URL="http://eurofurence.net/monof_tt.zip"
TEMP_DIR="$(mktemp -d -t --tmpdir=$TMPDIR )" || exit
FONT_DIRECTORY="$HOME/.fonts/truetype/"
trap "rm -rf -- '$TEMP_DIR'" EXIT

cd "$TEMP_DIR"
wget ${URL} -O ${FONT_NAME}.zip
unzip -o -j ${FONT_NAME}.zip
mkdir -p "$FONT_DIRECTORY"
# ls -halF "$TEMP_DIR"
cp *.ttf "$FONT_DIRECTORY"
fc-cache -f -v

cd "$cwd"
