#!/usr/bin/env python3

# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_path',required=True)
parser.add_argument('--key',required=True)
parser.add_argument('--percent',action='store_true')
parser.add_argument('--plot', action='store_true', help='Generate a plot')
parser.add_argument('--output_path', help='Path to save the plot, if not provided plot will be displayed')
parser.add_argument('--top', type=int, default=None, help='Show only the top N items')
parser.add_argument('--horizontal', action='store_true', help='Use horizontal bar chart')
args = parser.parse_args()



# imports
import os
import json
from collections import Counter,defaultdict

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
items = sorted(counts[args.key].items(), key=lambda item: (item[1],item[0]), reverse=True)
for k,v in items:
    print(k,':',v)



# Extract keys and values for plotting
    keys = [item[0] for item in items]
    values = [item[1] for item in items]
    
    # Create a single figure with a reasonable size
    fig = plt.figure(figsize=(10, 6 if args.horizontal else max(6, len(keys) * 0.3)))
    
    # Create bar chart
    if args.horizontal:
        # For horizontal bar chart, we reverse the order to have the highest value at the top
        plt.barh(keys[::-1], values[::-1])
        plt.xlabel('Count' + (' (%)' if args.percent else ''))
        plt.ylabel('Items')
    else:
        plt.bar(keys, values)
        plt.xlabel('Items')
        plt.ylabel('Count' + (' (%)' if args.percent else ''))
        # Rotate x-axis labels for better readability in vertical bar charts
        plt.xticks(rotation=45, ha='right')
    
    # Add title and tight layout
    plt.title(f'Distribution of {args.key}' + (' (%)' if args.percent else ''))
    plt.tight_layout()
    
    # Save or show the plot
    if args.output_path:
        plt.savefig(args.output_path)
        print(f"Plot saved to {args.output_path}")
    else:
        plt.show()
    
    # Close the figure after displaying or saving
    plt.close(fig)
