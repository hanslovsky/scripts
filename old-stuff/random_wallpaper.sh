#!/bin/bash




if [[ "$#" -lt "2" ]]; then
    echo "Wrong number of arguments"
    echo "Usage: $0 <wallpaper directory> <sleep time in seconds>"
    exit 1
fi



dir=$1
if [[ ! -d "$dir" ]]; then
    echo "$dir is not a diretory!"
    exit 2
fi
cd $dir
dir=`pwd`
cd "-" > /dev/null
files=$dir/*

sleep_time="$2s"

imgs=()
for f in $files; do
    python $HOME/git/scripts/check_if_image.py -f $f
    if [[ "$?" -eq "0" ]]; then
	imgs+=("$f")
    fi
done


n_images=${#imgs[@]}

set -e

while [[ "1" -eq "1" ]]; do
    index=`shuf -i1-$n_images -n1`
    img=${imgs[$index]}
    # ln -f -s $img $HOME/.wallpaper
    width=`identify -format "%[fx:w]" $img`
    height=`identify -format "%[fx:h]" $img`
    
    gsettings set org.gnome.desktop.background picture-uri file:///$img
    echo $img
    sleep $sleep_time
done
