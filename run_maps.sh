#!/bin/sh

# Process only zip files from September 20th through December
for file in /data/Twitter\ dataset/geoTwitter20-09-[2-3][0-9].zip /data/Twitter\ dataset/geoTwitter20-1[0-2]-*.zip; do
    echo "map file: $file"
    ./src/map.py --input_path="$file"
done
