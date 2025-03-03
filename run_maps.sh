#!/bin/sh

for file in /data/Twitter\ dataset/geoTwitter20-*.zip; do
	echo "map file: $file"
	./src/map.py --input_path="$file"
done
