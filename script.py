#!/usr/bin/env python3
import argparse
import os
import json
import re
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import glob
from collections import defaultdict

def parse_args():
    parser = argparse.ArgumentParser(description='Analyze Twitter data over time from multiple files')
    parser.add_argument('--input_dir', required=True, help='Directory containing the Twitter data files')
    parser.add_argument('--key', required=True, help='Key to analyze (e.g., language code or hashtag)')
    parser.add_argument('--output_path', default='twitter_trends.png', help='Path to save the visualization')
    parser.add_argument('--top', type=int, default=5, help='Number of top items to track')
    parser.add_argument('--percent', action='store_true', help='Show values as percentages')
    return parser.parse_args()

def extract_date_from_filename(filename):
    # Extract date from filenames like geoTwitter20-06-01.zip.lang
    match = re.search(r'geoTwitter(\d{2}-\d{2}-\d{2})', filename)
    if match:
        date_str = match.group(1)
        # Convert to datetime object (assuming 20 means 2020)
        return datetime.strptime(f'20{date_str}', '%Y-%m-%d')
    return None

def process_files(input_dir, key, percent=False):
    # Get all .lang files in the directory
    file_pattern = os.path.join(input_dir, '*.lang')
    files = glob.glob(file_pattern)
    
    if not files:
        print(f"No .lang files found in {input_dir}")
        return None
    
    # Dictionary to store time series data
    time_series = defaultdict(dict)
    
    # Process each file
    for file_path in sorted(files):
        try:
            # Extract date from filename
            filename = os.path.basename(file_path)
            date = extract_date_from_filename(filename)
            
            if not date:
                print(f"Could not extract date from {filename}, skipping")
                continue
            
            # Load data from file
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Check if key exists in data
            if key not in data:
                print(f"Key '{key}' not found in {filename}, skipping")
                continue
            
            # Extract counts for the key
            counts = data[key]
            
            # Normalize if requested
            if percent and '_all' in data:
                for k in counts:
                    counts[k] = counts[k] / data['_all'][k] * 100 if data['_all'][k] else 0
            
            # Add to time series
            for item, count in counts.items():
                time_series[item][date] = count
            
            print(f"Processed {filename}")
            
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    return time_series

def create_dataframe(time_series):
    # Convert the nested dictionary to a DataFrame
    df = pd.DataFrame.from_dict(time_series)
    
    # Sort the index (dates)
    df = df.sort_index()
    
    # Fill missing values with 0
    df = df.fillna(0)
    
    return df

def plot_top_items(df, top_n, output_path, key, percent=False):
    # Calculate the sum for each column to find top items
    column_sums = df.sum()
    top_columns = column_sums.nlargest(top_n).index.tolist()
    
    # Plot only the top columns
    plt.figure(figsize=(12, 8))
    
    for column in top_columns:
        plt.plot(df.index, df[column], marker='o', linewidth=2, label=column)
    
    # Formatting
    plt.xlabel('Date')
    ylabel = 'Percentage' if percent else 'Count'
    plt.ylabel(ylabel)
    plt.title(f'Top {top_n} Items for Key "{key}" Over Time')
    plt.legend(loc='best')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    
    # Save the figure
    plt.savefig(output_path)
    print(f"Plot saved to {output_path}")

def main():
    args = parse_args()
    
    # Process files and get time series data
    time_series = process_files(args.input_dir, args.key, args.percent)
    
    if not time_series:
        print("No data to visualize")
        return
    
    # Create DataFrame from time series
    df = create_dataframe(time_series)
    
    # Plot the top N items
    plot_top_items(df, args.top, args.output_path, args.key, args.percent)
    
    print("Analysis complete")

if __name__ == "__main__":
    main()
