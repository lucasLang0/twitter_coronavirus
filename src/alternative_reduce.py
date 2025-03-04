import os
import json
import matplotlib.pyplot as plt
import sys
from collections import defaultdict

def scan_data_files(hashtags, data_folder='outputs'):
    hashtag_data = defaultdict(lambda: defaultdict(int))
    
    for filename in os.listdir(data_folder):
        if filename.endswith('.lang'):
            with open(os.path.join(data_folder, filename), 'r') as file:
                data = json.load(file)
                date = filename.split('.')[0].split('geoTwitter')[1]
                for hashtag in hashtags:
                    if hashtag in data:
                        hashtag_data[hashtag][date] += sum(data[hashtag].values())
    
    return hashtag_data

def plot_data(hashtag_data, output_filename):
    plt.figure(figsize=(10, 6))
    
    for hashtag, data in hashtag_data.items():
        dates = sorted(data.keys())
        counts = [data[date] for date in dates]
        plt.plot(dates, counts, label=hashtag)
    
    plt.xlabel('Day of the Year')
    plt.ylabel('Number of Tweets')
    plt.title('Daily Usage of Hashtags')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_filename)
    plt.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python alternative_reduce.py <hashtag1> <hashtag2> ... <hashtagN>")
        sys.exit(1)
    
    hashtags = sys.argv[1:]
    hashtag_data = scan_data_files(hashtags)
    
    # Create a filename based on the hashtags
    output_filename = "_".join([hashtag.strip('#') for hashtag in hashtags]) + ".png"
    
    plot_data(hashtag_data, output_filename)
    
    print(f"Plot saved as {output_filename}")
