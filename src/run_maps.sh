#!/bin/bash

# Loop over each tweet file from 2020
for file in 2020*.zip; do
    echo "Processing $file..."
    nohup python3 map.py "$file" > "${file%.zip}.log" 2>&1 &
done

echo "All map.py processes started in parallel."
