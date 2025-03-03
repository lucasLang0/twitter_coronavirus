#!/usr/bin/env python3
# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_path', required=True)
parser.add_argument('--key', required=True)
parser.add_argument('--percent', action='store_true')
parser.add_argument('--plot', action='store_true', help='Generate a plot')
parser.add_argument('--output_path', help='Path to save the plot, if not provided plot will be displayed')
parser.add_argument('--top', type=int, default=10, help='Show only the top N items')
parser.add_argument('--horizontal', action='store_true', help='Use horizontal bar chart')
args = parser.parse_args()

# imports
import os
import json
from collections import Counter, defaultdict
import matplotlib
matplotlib.use('Agg')  # Set the backend to Agg
import matplotlib.pyplot as plt

# open the input path
with open(args.input_path) as f:
    counts = json.load(f)

# normalize the counts by the total values
if args.percent:
    for k in counts[args.key]:
        counts[args.key][k] /= counts['_all'][k]

# print the count values
items = sorted(counts[args.key].items(), key=lambda item: (item[1], item[0]), reverse=True)
for k, v in items:
    print(k, ':', v)

# Generate plot if requested
if args.plot:
    # Limit to top N items
    if args.top:
        items = items[:args.top]
    
    # Reverse for better visualization
    items.reverse()
    
    # Create plot
    if args.horizontal:
        plt.barh([item[0] for item in items], [item[1] for item in items])
    else:
        plt.bar([item[0] for item in items], [item[1] for item in items])
    
    plt.xlabel('Categories')
    plt.ylabel('Counts' if not args.percent else 'Percentage')
    title_suffix = f'Top {args.top} ' if args.top else ''
    plt.title(f'{title_suffix}countries that used {args.key} in 2020')
    plt.xticks(rotation=45)  # Rotate x-axis labels for better visibility
    plt.tight_layout()
    
    # Save or display the plot
    if args.output_path:
        plt.savefig(args.output_path, format='png')
    else:
        # Determine file type from key
        tag = args.key
        if tag.startswith('#'):
            tag = tag[1:]
        
        if 'lang' in args.input_path:
            plt.savefig(f"{tag}_language_count.png", format='png')
        else:
            plt.savefig(f"{tag}_country_count.png", format='png')
        
        print(f"Plot saved as {tag}_language_count.png or {tag}_country_count.png")
